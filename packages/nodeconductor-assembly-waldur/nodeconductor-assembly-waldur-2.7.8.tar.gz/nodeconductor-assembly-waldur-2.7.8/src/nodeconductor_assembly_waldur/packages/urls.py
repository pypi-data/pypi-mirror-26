from __future__ import unicode_literals

from nodeconductor_assembly_waldur.packages import views


def register_in(router):
    router.register(r'package-templates', views.PackageTemplateViewSet, base_name='package-template')
    router.register(r'openstack-packages', views.OpenStackPackageViewSet, base_name='openstack-package')
