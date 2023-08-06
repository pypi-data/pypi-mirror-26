# encoding: utf-8
import warnings
import time

from footmark.connection import ACSQueryConnection
from footmark.vpc.regioninfo import RegionInfo
from footmark.exception import VPCResponseError
from footmark.resultset import ResultSet
from footmark.vpc.vpc import Vpc
from footmark.vpc.eip import Eip
from footmark.vpc.vswitch import VSwitch
from footmark.vpc.router import RouteEntry, RouteTable
from footmark.vpc.config import *
from aliyunsdkcore.acs_exception.exceptions import ServerException


class VPCConnection(ACSQueryConnection):
    SDKVersion = '2014-05-26'
    DefaultRegionId = 'cn-hangzhou'
    DefaultRegionName = u'杭州'.encode("UTF-8")
    ResponseError = VPCResponseError

    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None,
                 region=None, sdk_version=None, security_token=None, user_agent=None):
        """
        Init method to create a new connection to ECS.
        """
        if not region:
            region = RegionInfo(self, self.DefaultRegionName,
                                self.DefaultRegionId)
        self.region = region
        if sdk_version:
            self.SDKVersion = sdk_version

        self.VPCSDK = 'aliyunsdkecs.request.v' + self.SDKVersion.replace('-', '')

        super(VPCConnection, self).__init__(acs_access_key_id=acs_access_key_id,
                                            acs_secret_access_key=acs_secret_access_key,
                                            region=self.region, product=self.VPCSDK,
                                            security_token=security_token, user_agent=user_agent)

    def build_filter_params(self, params, filters):
        if not isinstance(filters, dict):
            return

        flag = 1
        for key, value in filters.items():
            acs_key = key
            if acs_key.startswith('tag:'):
                while ('set_Tag%dKey' % flag) in params:
                    flag += 1
                if flag < 6:
                    params['set_Tag%dKey' % flag] = acs_key[4:]
                    params['set_Tag%dValue' % flag] = filters[acs_key]
                flag += 1
                continue
            if key == 'group_id':
                if not value.startswith('sg-') or len(value) != 12:
                    warnings.warn("The group-id filter now requires a security group "
                                  "identifier (sg-*) instead of a security group ID. "
                                  "The group-id " + value + "may be invalid.",
                                  UserWarning)
                params['set_SecurityGroupId'] = value
                continue
            if not isinstance(value, dict):
                acs_key = ''.join(s.capitalize() for s in acs_key.split('_'))
                params['set_' + acs_key] = value
                continue

            self.build_filters_params(params, value)

    def create_vpc(self, cidr_block=None, user_cidr=None, vpc_name=None, description=None, wait_timeout=None, wait=None):

        """
        Create a ECS VPC (virtual private cloud) in Aliyun Cloud
        :type cidr_block: String
        :param cidr_block: The cidr block representing the VPC, e.g. 10.0.0.0/8
        :type user_cidr: String
        :param user_cidr: User custom cidr in the VPC
        :type vpc_name: String
        :param vpc_name: A VPC name
        :type description: String
        :param description: Description about VPC
        :type wait: string
        :param wait: An optional bool value indicating wait for instance to be running before running
        :type wait_timeout: int
        :param wait_timeout: An optional int value indicating how long to wait, default 300
        :return: Returns details of created VPC
        """

        params = {}
        timeout = 20

        if cidr_block:
            self.build_list_params(params, cidr_block, 'CidrBlock')

        if user_cidr:
            self.build_list_params(params, user_cidr, 'UserCidr')

        if vpc_name:
            self.build_list_params(params, vpc_name, 'VpcName')

        if description:
            self.build_list_params(params, description, 'Description')

        response = self.get_object('CreateVpc', params, ResultSet)
        vpc_id = str(response.vpc_id)
        if str(wait).lower() in ['yes', 'true'] and wait_timeout:
            timeout = wait_timeout
        self.wait_for_vpc_status(vpc_id, 'Available', 4, timeout)

        return self.get_vpc_attribute(vpc_id)

    def get_vpc_attribute(self, vpc_id):
        """
        method to get all vpcId of particular region 
        :return: Return All vpcs in the region
        """
        vpcs = self.get_all_vpcs(vpc_id=vpc_id)
        if vpcs:
            return vpcs[0]

        return None

    def get_all_vpcs(self, vpc_id=None, is_default=None, pagenumber=1, pagesize=10):
        """
        Find Vpc in One Region
        :type vpc_id: string
        :param vpc_id: Vpc Id of the targeted Vpc to terminate
        :type is_default: bool
        :param is_default: The vpc created by system if it is True
        :type pagenumber: integer
        :param pagenumber: Page number of the instance status list. The start value is 1. The default value is 1
        :type pagesize: integer
        :param pagesize: Sets the number of lines per page for queries per page. The maximum value is 50.
        The default value is 10
        :rtype: list
        :return: Returns VPC list if vpcs found along with Vpc details.
        """
        params = {}

        if vpc_id:
            self.build_list_params(params, vpc_id, 'VpcId')

        if is_default is not None:
            self.build_list_params(params, is_default, 'IsDefault')

        self.build_list_params(params, pagenumber, 'PageNumber')
        self.build_list_params(params, pagesize, 'PageSize')

        return self.get_list('DescribeVpcs', params, ['Vpcs', Vpc])

    def modify_vpc(self, vpc_id, vpc_name=None, description=None, user_cidr=None, wait_timeout=None, wait=None):

        """
        Modify a ECS VPC's (virtual private cloud) attribute in Aliyun Cloud
        :type vpc_id: string
        :param vpc_id: Vpc Id of the targeted Vpc to modify
        :type vpc_name: String
        :param vpc_name: A VPC name
        :type description: String
        :param description: Description about VPC
        :type user_cidr: String
        :param user_cidr: User custom cidr in the VPC
        :type wait: string
        :param wait: An optional bool value indicating wait for instance to be running before running
        :type wait_timeout: int
        :param wait_timeout: An optional int value indicating how long to wait, default 300
        :return: Returns details of created VPC
        """

        params = {}
        self.build_list_params(params, vpc_id, 'VpcId')

        if user_cidr:
            self.build_list_params(params, user_cidr, 'UserCidr')

        if vpc_name:
            self.build_list_params(params, vpc_name, 'VpcName')

        if description:
            self.build_list_params(params, description, 'Description')

        self.get_status('ModifyVpcAttribute', params)

        timeout = 16
        if str(wait).lower() in ['yes', 'true'] and wait_timeout:
            timeout = wait_timeout
        self.wait_for_vpc_status(vpc_id, 'Available', 4, timeout)

        return self.get_vpc_attribute(vpc_id)

    def delete_vpc(self, vpc_id):
        """
        Delete Vpc
        :type vpc_id: string
        :param vpc_id: Vpc Id of the targeted Vpc to terminate
        :rtype: bool
        :return: Return result of deleting.
       """
        changed = False

        params = {}

        self.build_list_params(params, vpc_id, 'VpcId')

        if self.wait_for_vpc_status(vpc_id, 'Available', 4, 16):
            changed = self.get_status('DeleteVpc', params)

        return changed

    def create_vswitch(self, zone_id, vpc_id, cidr_block, vswitch_name=None, description=None):
        """
        :type zone_id: String
        :param zone_id: Required parameter. ID of the zone to which an VSwitch belongs
        :type vpc_id: String
        :param vpc_id: Required parameter. The VPC ID of the new VSwitch
        :type cidr_block: String
        :param cidr_block: Required parameter. The cidr block representing the VSwitch, e.g. 10.0.0.0/8
        :type vswitch_name: String
        :param vswitch_name: A VSwitch name
        :type description: String
        :param description: Description about VSwitch
        
        :return: Return the operation result and details of created VSwitch
        """
        params = {}

        self.build_list_params(params, vpc_id, 'VpcId')
        self.build_list_params(params, zone_id, 'ZoneId')
        self.build_list_params(params, cidr_block, 'CidrBlock')

        if vswitch_name:
            self.build_list_params(params, vswitch_name, 'VSwitchName')

        if description:
                self.build_list_params(params, description, 'Description')

        response = self.get_object('CreateVSwitch', params, ResultSet)
        vsw_id = str(response.vswitch_id)
        changed = self.wait_for_vswitch_status(vsw_id, 'Available', 4, 16)
        return changed, self.get_vswitch_attribute(vsw_id)

    def get_all_vswitches(self, vpc_id=None, vswitch_id=None, zone_id=None, is_default=None, pagenumber=1, pagesize=10):
        """
        Find Vpc
        :type vpc_id: String
        :param vpc_id: The VPC ID of the VSwitch
        :type vswitch_id: String
        :param vswitch_id: ID of the specified VSwitch
        :type zone_id: String
        :param zone_id: ID of the zone to which an VSwitch belongs
        :type is_default: bool
        :param is_default: The vswitch created by system if it is True
        :type pagenumber: integer
        :param pagenumber: Page number of the instance status list. The start value is 1. The default value is 1
        :type pagesize: integer
        :param pagesize: Sets the number of lines per page for queries per page. The maximum value is 50.
        The default value is 10
        :rtype: list
        :return: Return VSwitch list if VSwitches found along with VSwitch details.
        """
        params = {}

        if vpc_id:
            self.build_list_params(params, vpc_id, 'VpcId')

        if vswitch_id:
            self.build_list_params(params, vswitch_id, 'VSwitchId')

        if zone_id:
            self.build_list_params(params, zone_id, 'ZoneId')

        if is_default is not None:
            self.build_list_params(params, is_default, 'IsDefault')

        self.build_list_params(params, pagenumber, 'PageNumber')
        self.build_list_params(params, pagesize, 'PageSize')

        return self.get_list('DescribeVSwitches', params, ['VSwitches', VSwitch])

    def get_vswitch_attribute(self, vswitch_id):
        """
        method to get specified vswitch attribute 
        :return: Return vswitch with its attribute
        """

        response = self.get_all_vswitches(vswitch_id=vswitch_id)
        if response:
            return response[0]

        return None

    def modify_vswitch(self, vswitch_id, vswitch_name=None, description=None):
        """
        :type vswitch_id: String
        :param vswitch_id: Required parameter. The VSwitch ID.
        :type vswitch_name: String
        :param vswitch_name: A VSwitch name
        :type description: String
        :param description: Description about VSwitch
        
        :return: Return the operation result and details of modified VSwitch
        """
        params = {}

        self.build_list_params(params, vswitch_id, 'VSwitchId')

        if vswitch_name:
            self.build_list_params(params, vswitch_name, 'VSwitchName')

        if description:
            self.build_list_params(params, description, 'Description')

        self.get_status('ModifyVSwitchAttribute', params)
        self.wait_for_vswitch_status(vswitch_id, 'Available', 4, 16)
        return self.get_vswitch_attribute(vswitch_id)

    def delete_vswitch(self, vswitch_id):
        """
        Delete VSwitch
        :type vswitch_id : str
        :param vswitch_id: The Id of vswitch
        :rtype bool
        :return: return result of deleting
        """

        changed = False
        delay = 4
        timeout = 20

        params = {}

        self.build_list_params(params, vswitch_id, 'VSwitchId')

        if self.wait_for_vswitch_status(vswitch_id, 'Available', delay, timeout):
            while timeout > 0:
                try:
                    changed = self.get_status('DeleteVSwitch', params)
                    break
                except ServerException as e:
                    if e.error_code == DependencyViolation:
                        print "Specified vswitch %s has dependent resources - try again" % vswitch_id
                        timeout -= delay
                        if timeout <= 0:
                            raise Exception("Timeout Error: Waiting for deleting specified vswitch %s." % vswitch_id)

                        time.sleep(delay)

        return changed

    def delete_vswitch_with_vpc(self, vpc_id):
        """
        Delete VSwitches in the specified VPC
        :type vpc_id : str
        :param vpc_id: The Id of vpc to which vswitch belongs
        :rtype list
        :return: return list ID of deleted VSwitch
        """

        vswitch_ids = []
        if not vpc_id:
                raise Exception(msg="It must be specify vpc_id.")

        vswitches = self.get_all_vswitches(vpc_id=vpc_id)
        for vsw in vswitches:
            vsw_id = str(vsw.id)
            if self.delete_vswitch(vsw_id):
                vswitch_ids.append(vsw_id)

        return vswitch_ids

    def create_route_entry(self, route_table_id, destination_cidrblock, nexthop_type=None, nexthop_id=None, nexthop_list=None):
        """
        Create RouteEntry for VPC
        :type route_table_id: str
        :param route_table_id: ID of route table in the VPC
        :type destination_cidrblock: str
        :param destination_cidrblock: The destination CIDR of route entry. It must be a legal CIDR or IP address, such as: 192.168.0.0/24 or 192.168.0.1
        :type nexthop_type: str
        :param nexthop_type: The type of next hop. Available value options: Instance, Tunnel, HaVip, RouterInterface. Default is Instance.
        :type next_hop_id: str
        :param next_hop_id: The ID of next hop.
        :type nexthop_list: str
        :param nexthop_list: The route item of next hop list. 
        :rtype 
        :return Return result of Creating RouteEntry.
        """
        params = {}

        self.build_list_params(params, route_table_id, 'RouteTableId')
        self.build_list_params(params, destination_cidrblock, 'DestinationCidrBlock')

        if nexthop_type:
            self.build_list_params(params, nexthop_type, 'NextHopType')

        if nexthop_id:
            self.build_list_params(params, nexthop_id, 'NextHopId')

        if nexthop_list:
            self.build_list_params(params, nexthop_list, 'NextHopList')

        if self.get_status('CreateRouteEntry', params)\
                and self.wait_for_route_entry_status(route_table_id, destination_cidrblock, 'Available', 4, 16):

            return self.get_route_entry_attribute(route_table_id, destination_cidrblock)

        return None

    def get_route_entry_attribute(self, route_table_id, destination_cidrblock, nexthop_id=None):
        """
        Querying route entry attribute
        :type route_table_id: str
        :param route_table_id: ID of route table in the VPC
        :type destination_cidrblock: str
        :param destination_cidrblock: The destination CIDR of route entry. It must be a legal CIDR or IP address, such as: 192.168.0.0/24 or 192.168.0.1
        :type nexthop_id: str
        :param nexthop_type: The ID of next hop.
        :rtype 
        :return: VRouters in json format
        """

        route_entries = self.get_all_route_entries(route_table_id=route_table_id)
        if route_entries:
            for entry in route_entries:
                if destination_cidrblock == str(entry.destination_cidrblock):
                    return entry
        return None

    def get_all_route_entries(self, router_id=None, router_type=None, route_table_id=None, pagenumber=1, pagesize=10):
        """
        Querying all route entries in the specified router or route_tables_id
        :type router_id: str
        :param router_id: The ID of router which is to be fetched.
        :type router_type str
        :param router_type: The type of router which is to be fetched.
        :type route_table_id: str
        :param route_table_id: ID of route table in one VPC
        :type pagenumber: integer
        :param pagenumber: Page number of the route table list. The start value is 1. The default value is 1
        :type pagesize: integer
        :param pagesize: Sets the number of lines per page for queries per page. The maximum value is 50.
        The default value is 10 
        :rtype list<>
        :return: List of route entry.
        """
        route_tables = self.get_all_route_tables(router_id=router_id, router_type=router_type, route_table_id=route_table_id,
                                                 pagenumber=pagenumber, pagesize=pagesize)
        route_entries = []
        if route_tables:
            for table in route_tables:
                if table.route_entrys:
                    for entry in table.route_entrys['route_entry']:
                        route_entry = RouteEntry(self)
                        for k, v in entry.items():
                            setattr(route_entry, k, v)
                        route_entries.append(route_entry)

        return route_entries

    def delete_route_entry(self, route_table_id, destination_cidrblock=None, nexthop_id=None, nexthop_list=None):
        """
        Deletes the specified RouteEntry for the vpc
        :type route_table_id: str
        :param route_table_id: ID of route table in the VPC
        :type destination_cidrblock: str
        :param destination_cidrblock: The destination CIDR of route entry. It must be a legal CIDR or IP address, such as: 192.168.0.0/24 or 192.168.0.1
        :type next_hop_id: str
        :param next_hop_id: The ID of next hop.
        :type nexthop_list: str
        :param nexthop_list: The route item of next hop list.
        :rtype bool
        :return Return result of deleting route entry.
        """
        params = {}

        self.build_list_params(params, route_table_id, 'RouteTableId')
        if destination_cidrblock:
            self.build_list_params(params, destination_cidrblock, 'DestinationCidrBlock')

        if nexthop_id:
            self.build_list_params(params, nexthop_id, 'NextHopId')

        if nexthop_list:
            self.build_list_params(params, nexthop_list, 'NextHopList')

        return self.get_status('DeleteRouteEntry', params)

    def get_route_table_attribute(self, route_table_id):
        """
        Querying route table attribute
        :type route_table_id: str
        :param route_table_id: ID of route table in the VPC
        :rtype dict
        :return: VRouters in json format
        """
        return self.get_all_route_tables(route_table_id=route_table_id)

    def get_all_route_tables(self, router_id=None, router_type=None, route_table_id=None, pagenumber=1, pagesize=10):
        """
        Querying vrouter
        :type router_id: str
        :param router_id: The ID of router which is to be fetched.
        :type router_type str
        :param router_type: The type of router which is to be fetched.
        :type route_table_id: str
        :param route_table_id: ID of route table in one VPC
        :type pagenumber: integer
        :param pagenumber: Page number of the route entry list. The start value is 1. The default value is 1
        :type pagesize: integer
        :param pagesize: Sets the number of lines per page for queries per page. The maximum value is 50.
        The default value is 10 
        :rtype list<>
        :return: List of route entry.
        """
        params = {}

        if router_id:
            self.build_list_params(params, router_id, 'RouterId')

        if router_type:
            self.build_list_params(params, router_type, 'RouterType')

        if route_table_id:
            self.build_list_params(params, route_table_id, 'RouteTableId')

        if pagenumber:
            self.build_list_params(params, pagenumber, 'PageNumber')

        if pagesize:
            self.build_list_params(params, pagesize, 'PageSize')

        return self.get_list('DescribeRouteTables', params, ['RouteTables', RouteTable])

    def get_instance_info(self):
        """
        method to get all Instances of particular region 
        :return: Return All Instances in the region
        """
        params = {}
        results = []

        try:
            v_ids = {}
            response = self.get_status('DescribeInstances', params)
            results.append(response)
            
        except Exception as ex:        
            error_code = ex.error_code
            error_msg = ex.message
            results.append({"Error Code": error_code, "Error Message": error_msg})

        return results

    def allocate_eip_addresses(self, bandwidth, internet_charge_type):
        """
        method to query eip addresses in the region
        :type bandwidth : str
        :param bandwidth : bandwidth of the eip address
        :type internet_charge_type : str
        :param internet_charge_type : paybytraffic or paybybandwidth types
        :return: Return the allocationId , requestId and EIP address
        """
        params = {}
        results = {}
        changed = False
        if bandwidth:
            self.build_list_params(params, bandwidth, 'Bandwidth')
            
        if internet_charge_type:
            self.build_list_params(params, internet_charge_type, 'InternetChargeType')
                  
        results = self.get_object('AllocateEipAddress', params, ResultSet)
        eips = self.describe_eip_address(eip_address = results.eip_address, allocation_id = results.allocation_id)
        changed = True
        
        return changed, eips.eip_addresses["eip_address"][0]

    def bind_eip(self, allocation_id, instance_id):
        """
        :type allocation_id:string
        :param allocation_id:The instance ID of the EIP
        :type instance_id:string
        :param instance_id:The ID of an ECS instance
        :return:Returns the status of operation
        """
        params = {}
        result = False
        
        self.build_list_params(params, allocation_id, 'AllocationId')
        self.build_list_params(params, instance_id, 'InstanceId')
       
        self.get_object('AssociateEipAddress', params, ResultSet)
        return self.wait_for_eip_status(allocation_id=allocation_id, status="InUse")    

    def unbind_eip(self, allocation_id, instance_id):
        """
        :type allocation_id:string
        :param allocation_id:The instance ID of the EIP
        :type instance_id:string
        :param instance_id:The ID of an ECS instance
        :return:Request Id
        """
        params = {}
        result = False
        if allocation_id:
            self.build_list_params(params, allocation_id, 'AllocationId')
        if instance_id:
            self.build_list_params(params, instance_id, 'InstanceId')
        results = self.get_object('UnassociateEipAddress', params, ResultSet)
        if results.request_id:
            result = self.wait_for_eip_status(allocation_id=allocation_id, status="Available")  

        return result
        
    def modifying_eip_attributes(self, allocation_id, bandwidth):
        """
        :type allocation_id:string
        :param allocation_id:The instance ID of the EIP
        :type bandwidth:string
        :param bandwidth:Bandwidth of the EIP instance
        :return:Request Id
        """
        params = {}
        results = []
        changed = False

        if allocation_id:
            self.build_list_params(params, allocation_id, 'AllocationId')
        if bandwidth:
            self.build_list_params(params, bandwidth, 'Bandwidth')
        results = self.get_status('ModifyEipAddressAttribute', params)
        changed = True
        
        return changed, results

    def get_all_vrouters(self, vrouter_id=None, pagenumber=None, pagesize=None):
        """
        Querying vrouter
        :param vrouter_id: VRouter_Id to be fetched
        :type vrouter_id: str
        :type pagenumber: integer
        :param pagenumber: Page number of the instance status list. The start value is 1. The default value is 1
        :type pagesize: integer
        :param pagesize: Sets the number of lines per page for queries per page. The maximum value is 50.
        The default value is 10
        :return: VRouters in json format
        """
        params = {}
        results = []

        try:
            if vrouter_id is not None :
                self.build_list_params(params, vrouter_id, 'VRouterId')

            if pagenumber is not None :
                self.build_list_params(params, pagenumber, 'PageNumber')

            if pagesize is not None :
                self.build_list_params(params, pagesize, 'PageSize')

            results = self.get_status('DescribeVRouters', params)
        except Exception as ex:
            error_code = ex.error_code
            error_msg = ex.message
            results.append({"Error Code": error_code, "Error Message": error_msg})

        return False, results

    def releasing_eip(self, allocation_id):
        """
        To release Elastic Ip
        :type allocation_id: string
        :param allocation_id: To release the allocation ID,allocation ID uniquely identifies the EIP
        :return: Return status of operation
        """
        params = {}
        results = []
        describe_eip = []
        result = False

        self.build_list_params(params, allocation_id, 'AllocationId')
        results = self.get_object('ReleaseEipAddress', params, ResultSet)
        if results.request_id:
            result = True
             
        return result
    
    def wait_condition(self, delayTime, timeOut, condition):
        tm = 0
        assert(delayTime > 0)
        assert(timeOut > delayTime)
        while tm < timeOut:
            if condition(tm):
                return True
            tm = tm + delayTime
            time.sleep(delayTime)
        return False        
               
    def wait_for_eip_status(self, eip_address = None, allocation_id=None, status = "", delayTime = 1, timeOut = 8):
        """
        wait for bind ok
        :param eip_address:
        :param allocation_id:
        :param status:
        :return: 
        """
        params = {}
        result = False

        if allocation_id:
            self.build_list_params(params, allocation_id, 'AllocationId')
        if eip_address:
            self.build_list_params(params, eip_address, 'EipAddress')

        condition = lambda s :status == self.get_object('DescribeEipAddresses', params, ResultSet).eip_addresses['eip_address'][0]['status']
        result = self.wait_condition(delayTime, timeOut, condition)
        return result

    def describe_eip_address(self, eip_address=None, allocation_id=None, eip_status=None,
                             page_number=1, page_size=10):
        """
        Get EIP details for a region
        :param eip_address:
        :param allocation_id:
        :param eip_status:
        :return:
        """
        params = {}
        eip_details=None

        if allocation_id:
            self.build_list_params(params, allocation_id, 'AllocationId')
        if eip_address:
            self.build_list_params(params, eip_address, 'EipAddress')
        if eip_status:
            self.build_list_params(params, eip_status, 'Status')

        self.build_list_params(params, page_number, 'PageNumber')
        self.build_list_params(params, page_size, 'PageSize')
        
        return self.get_list('DescribeEipAddresses', params, ['eip', Eip])


    def get_vswitch_status(self, vpc_id, zone_id=None, vswitch_id=None, pagenumber=None, pagesize=None):
        """
        List VSwitches of VPC with their status
        :type vpc_id: string
        :param vpc_id: ID of Vpc from which VSwitch belongs
        :type zone_id: string
        :param zone_id: ID of the Zone
        :type vswitch_id: string
        :param vswitch_id: The ID of the VSwitch to be queried
        :type pagenumber: integer
        :param pagenumber: Page number of the instance status list. The start value is 1. The default value is 1
        :type pagesize: integer
        :param pagesize: The number of lines per page set for paging query. The maximum value is 50 and default
        value is 10
        :return: Returns list of vswitches in VPC with their status
        """
        params = {}
        results = []

        self.build_list_params(params, vpc_id, 'VpcId')
        if zone_id:
            self.build_list_params(params, zone_id, 'ZoneId')
        if vswitch_id:
            self.build_list_params(params, vswitch_id, 'VSwitchId')
        if pagenumber:
            self.build_list_params(params, pagenumber, 'PageNumber')
        if pagesize:
            self.build_list_params(params, pagesize, 'PageSize')

        try:
            results = self.get_status('DescribeVSwitches', params)
        except Exception as ex:
            error_code = ex.error_code
            error_msg = ex.message
            results.append({"Error Code": error_code, "Error Message": error_msg})

        return False, results

    def wait_for_vpc_status(self, vpc_id, status, delay=DefaultWaitForInterval, timeout=DefaultTimeOut):

        try:
            while True:
                vpc = self.get_vpc_attribute(vpc_id)
                if vpc and str(vpc.status) in [status, str(status).lower()]:
                    return True

                timeout -= delay

                if timeout <= 0:
                    raise Exception("Timeout Error: Waiting for VPC status is %s, time-consuming %d seconds." % (status, timeout))

                time.sleep(delay)
        except Exception as e:
            raise e

    def wait_for_vswitch_status(self, vswitch_id, status, delay=DefaultWaitForInterval, timeout=DefaultTimeOut):
        try:
            while True:
                vsw = self.get_vswitch_attribute(vswitch_id)
                if vsw and str(vsw.status) in [status, str(status).lower()]:
                    return True

                timeout -= delay

                if timeout <= 0:
                    raise Exception("Timeout Error: Waiting for VSwitch status is %s, time-consuming %d seconds." % (status, timeout))

                time.sleep(delay)
        except Exception as e:
            raise e

    def wait_for_route_entry_status(self, route_table_id, destination_cidrblock, status, delay=DefaultWaitForInterval, timeout=DefaultTimeOut):
        try:
            while True:
                route_entry = self.get_route_entry_attribute(route_table_id, destination_cidrblock)
                if route_entry and str(route_entry.status) in [status, str(status).lower()]:
                    return True

                timeout -= delay

                if timeout <= 0:
                    raise Exception("Timeout Error: Waiting for route entry status is %s, time-consuming %d seconds." % (status, timeout))

                time.sleep(delay)
        except Exception as e:
            raise e
