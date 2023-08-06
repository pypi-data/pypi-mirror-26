import json
from pathlib import Path
from subprocess import check_call


class Packer():
    def __init__(self, packer_dir="./packer", var_file='vars.json'):
        self.packer_dir = Path(packer_dir)
        vars_file = self.packer_dir / var_file
        if vars_file.exists():
            with vars_file.open() as data_file:
                self.vars = json.load(data_file)

    def get_var(self, key):
        return self.vars[key]


    def check_sudo(cmd, **kwargs):
        return check_call(["sudo"] + cmd, **kwargs)


    def check_as(cmd, check=check_call, **kwargs):
        def demote(user_uid, user_gid):
            def set_ids():
                os.setgid(user_gid)
                os.setuid(user_uid)

            return set_ids

        return check(cmd, preexec_fn=demote(1000, 1000), **kwargs)


    def mkdir(dir, *, own=None, mod=None, uid=None, gid=None):
        check_call(["sudo", "mkdir", "-p", dir])
        if own is None:
            if uid is None:
                uid = str(os.getuid())
            if gid is None:
                gid = str(os.getgid())
            own = f"{uid}:{gid}"
        check_sudo(["chown", own, dir])
        if mod is not None:
            check_sudo(["chmod", mod, dir])


    def mv(vars, src, dest, *, own=None, mod=None, src_dir=None):
        if src_dir is None:
            src_dir = vars['packer_dir']
        check_sudo(["mv", f"{src_dir}/{src}", dest])
        if own is not None:
            check_sudo(["chown", own, f"{dest}/{src}"])
        if mod is not None:
            check_sudo(["chmod", mod, f"{dest}/{src}"])


    def install_nginx(packer_dir, conf_files):
        check_sudo(["rm", "/etc/nginx/sites-enabled/default"])
        for file in conf_files:
            check_sudo(["mv", f"{packer_dir}/{file}", f"/etc/nginx/sites-available/{file}"])
            check_sudo(["ln", "-s", f"/etc/nginx/sites-available/{file}", f"/etc/nginx/sites-enabled/{file}"])
        out = str(check_output(["nginx", "-v"], stderr=STDOUT, universal_newlines=True))
        return out.split('/')[1].split()[0] + " (configuration files in /etc/nginx/sites-enabled/)"
