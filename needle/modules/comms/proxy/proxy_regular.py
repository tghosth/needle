from __future__ import unicode_literals
from core.framework.module import BaseModule
from core.utils.utils import Utils


class Module(BaseModule):
    meta = {
        'name': 'Intercepting Proxy',
        'author': '@LanciniMarco (@MWRLabs)',
        'description': 'Intercept the traffic generated by the device. Read the comments below before starting.',
        'options': (
            ('port', 9090, True, 'Proxy service port.'),
            ('verbose', False, True, 'Verbose output (print the HTTP headers of every request/response).'),
            ('anticache', True, True, 'Strip out request headers that might cause the server to return 304-not-modified.'),
            ('output', True, False, 'Full path of the output dump file.'),
            ('upstream_ip', False, False, 'Upstream proxy server IP (to forward all requests to).'),
            ('upstream_port', False, False, 'Upstream proxy server PORT (to forward all requests to).'),
            ('target_domain', "", False, 'Comma separated list of the domains to analyze (Example: domain.com,other.com). If empty, everything will be in scope.'),
        ),
        'comments': ['Connect this workstation and the device to the same Wi-Fi',
                     'Configure the device to use this host as proxy',
                     'Run `comms/certs/install_ca_mitm` to install the CA Certificate of MitmProxy on the device',
                     'Notice that, due to a current bug in Mitmproxy, if an upstream proxy is set, the logging functionality will not work (i.e., the output file will be empty)']
    }

    # ==================================================================================================================
    # UTILS
    # ==================================================================================================================
    def __init__(self, params):
        BaseModule.__init__(self, params)
        # Setting default output file
        self.options['output'] = self.local_op.build_output_path_for_file("proxy_regular.out", self)

    def module_pre(self):
        return BaseModule.module_pre(self, bypass_app=True)

    # ==================================================================================================================
    # RUN
    # ==================================================================================================================
    def module_run(self):
        # Parse variables
        port = self.options['port']
        verbose = self.options['verbose']
        anticache = self.options['anticache']
        output = self.options['output']
        upstream_ip = self.options['upstream_ip']
        upstream_port = self.options['upstream_port']
        target_domain = self.options['target_domain']

        # Check upstream
        upstream_list = [upstream_ip, upstream_port]
        if None in upstream_list or False in upstream_list:
            upstream = False
            if any(upstream_list):
                self.printer.error('Please specify both the IP and PORT of the upstream proxy (or remove them both).')
                return
        else:
            upstream = True

        # Build command string
        cmd = "{proxyapp} -p {port}".format(proxyapp=self.TOOLS_LOCAL['MITMDUMP'],
                                            port=port)
        if verbose: cmd += ' -d'
        if anticache: cmd += ' --anticache'
        if output: cmd += ' --wfile {}'.format(output)
        if upstream: cmd += ' --upstream http://{ip}:{port}'.format(ip=upstream_ip, port=upstream_port)
        if target_domain:
            domain_list = map(Utils.regex_escape_str, target_domain.split(','))
            domain_list_string = ''.join(['(?!{})'.format(el) for el in domain_list])
            cmd += " --ignore '^{}'".format(domain_list_string)

        # Intercept
        self.printer.notify('Configure the device to use this host as proxy: {ip}:{port}'.format(ip=self.local_op.get_ip(), port=port))
        self.printer.info('Starting intercepting proxy. Press Ctrl-c to quit.')
        self.local_op.command_interactive(cmd)
