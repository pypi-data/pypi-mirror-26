Radware NG driver for Openstack Liberty Neutron LBaaS v2
-----------------------------------------------------

This is the Radware driver for
OpenStack Neutron LOADBALANCER service v2, Newton release.

In order to activate Radware's lbaas provider, perform following steps:

    1. Install the radware_os_lb_v2_newton package by executing the following command (use sudo if needed):
       
       pip install radware_os_lb_v2_newton

    2. Open the neutron configuration file named neutron_lbaas.conf.
       Under [service_providers] section, next to Haproxy LOADBALANCERV2 provider,
       add new line, declaring the Radware LOADBALANCER v2 provider.
       
       service_provider = LOADBALANCERV2:radwarev2:radware_os_lb_v2_newton.v2_driver.RadwareLBaaSV2Driver:default

       To keep the HAproxy provider as a default LOADBALANCERV2 provider, 
       remove the attribute :default from the Radware LOADBALANCERV2 provider line.
       Otherwise, remove the :default attribute of the HAproxy LOADBALNCERV2 provider line. 

    3. Add new section called [radwarev2] at the end of neutron configuration file named neutron.conf.
       Add following Radware LOADBALANCERV2 parameters under the section:
           
           vdirect_address = < Your vDirect server IP address > 

    4. For additional Radware LBaaS configuration parameters,
       please see the documentation

    5. Restart the neutron-server service

Following is an example of neutron_lbaas.conf file after editing:

    [service_providers]

    service_provider=LOADBALANCERV2:Haproxy:neutron_lbaas.drivers.haproxy.plugin_driver.HaproxyOnHostPluginDriver:default
    service_provider=LOADBALANCERV2:radwarev2:radware_os_lb_v2_newton.v2_driver.RadwareLBaaSV2Driver

Following is an example of neutron.conf file after editing:

    [radwarev2]
    vdirect_address=< Your vDirect server IP address >

