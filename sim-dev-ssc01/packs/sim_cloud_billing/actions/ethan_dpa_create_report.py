import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time
from datetime import date, timedelta
from lxml import etree
from io import StringIO
from st2common.runners.base_action import Action

class CreateDPAReportAction(Action):
    def __init__(self, config):
        super(CreateDPAReportAction, self).__init__(config)

    def run(self, report_name, input_start_date=None, input_finish_date=None):
        if not input_start_date and not input_finish_date:
            input_finish_date = date.today().replace(day=1) - timedelta(days=1)
            input_start_date = date.today().replace(day=1) - timedelta(days=input_finish_date.day)
        print(input_start_date)
        print(input_finish_date)

        self.report_name       = report_name
        self.input_start_date  = input_start_date
        self.input_finish_date = input_finish_date
        self.nodes             = self.get_nodes()
        report_location        = self.create_report()
        return self.transform_xml(self.retrieve_report(report_location))

    def get_nodes(self):
        try:
            endpoint = "{}/apollo-api/nodes/?query=globalName=*CUSTID*".format(self.config['dpa']['host'])
            session = requests.Session()
            session.auth = (self.config['dpa']['username'], self.config['dpa']['password'])
            response = session.get(url=endpoint, verify=False)
            response.raise_for_status()
            if response.text:
                xslt_root = etree.XML("<xsl:stylesheet xmlns:xsl=\"http://www.w3.org/1999/XSL/Transform\" version=\"1.0\"><xsl:output indent=\"no\" /><xsl:template match=\"/\"><xsl:variable name=\"CUSTID\" select=\"//node[name='CUSTID']/id\" /><nodes><xsl:for-each select=\"//node[partOfId=$CUSTID]\"><node><id><xsl:value-of select=\"id\" disable-output-escaping=\"no\" /></id></node></xsl:for-each></nodes></xsl:template></xsl:stylesheet>")
                transform = etree.XSLT(xslt_root)
                input_xml = etree.parse(StringIO(response.text))
                result = transform(input_xml)
                return etree.tostring(result, encoding='unicode')
            return None
        except Exception as e:
            raise Exception(e)

    def retrieve_report(self, endpoint):
        try:
            session = requests.Session()
            session.auth = (self.config['dpa']['username'], self.config['dpa']['password'])
            response = session.get(url=endpoint, verify=False)
            print(response.status_code)
            while response.status_code != 200:
                time.sleep(30)
                return self.retrieve_report(endpoint)
            return response.text
        except Exception as e:
            raise Exception(e)

    def create_report(self):
        try:
            data = "<runReportParameters><report><name>{}</name></report><nodeLinks><nodeLink type=\"Group\"><id>00000000-0000-0000-0000-000000000001</id><name>Root</name><child type=\"Group\"><id>00000000-0000-0000-0000-000000000010</id><name>Groups</name><child type=\"Group\"><name>Configuration</name><id>8ad04346-9abd-4466-8bd8-05306b63519d</id><child type=\"Group\"><name>Servers</name><id>307c9831-e611-453d-bbb8-89ff3e0248b7</id><child type=\"Group\"><name>Backup Servers</name><id>c5723b8f-c5b7-4237-af29-b689203fbc44</id><child type=\"Group\"><name>EMC Avamar</name><id>a58abe61-ad35-4365-ab91-b53afa54e294</id></child></child></child></child></child></nodeLink><nodeLink type=\"Group\"><id>00000000-0000-0000-0000-000000000001</id><name>Root</name><child type=\"Group\"><id>00000000-0000-0000-0000-000000000010</id><name>Groups</name><child type=\"Group\"><name>Configuration</name><id>8ad04346-9abd-4466-8bd8-05306b63519d</id><child type=\"Group\"><name>Servers</name><id>307c9831-e611-453d-bbb8-89ff3e0248b7</id><child type=\"Group\"><name>Protection Servers</name><id>dadcdfdb-5969-4b9e-885b-21f6d1fb47da</id><child type=\"Group\"><name>PowerProtect Data Manager</name><id>1d24abaf-c0bb-478f-a34b-12dc7534218b</id></child></child></child></child></child></nodeLink></nodeLinks><timeConstraints type=\"absolute\"><startTime date=\"{}\" time=\"00:00:00.000\" tzid=\"Australia/Sydney\"/><endTime date=\"{}\" time=\"23:59:00.000\" tzid=\"Australia/Sydney\"/></timeConstraints><formatParameters><formatType>RawXML</formatType><fitContent>false</fitContent></formatParameters><user><logonName>administrator</logonName></user><runInDebug>false</runInDebug></runReportParameters>".format(self.report_name, self.input_start_date, self.input_finish_date)
            if self.report_name.lower() == 'ccb usage report':
                data = "<runReportParameters><report><name>{}</name></report>{}<timeConstraints type=\"absolute\"><startTime date=\"{}\" time=\"00:00:00.000\" tzid=\"Australia/Sydney\"/><endTime date=\"{}\" time=\"23:59:00.000\" tzid=\"Australia/Sydney\"/></timeConstraints><formatParameters><formatType>RawXML</formatType></formatParameters><user><logonName>administrator</logonName></user><runInDebug>false</runInDebug></runReportParameters>".format(self.report_name, self.nodes, self.input_start_date, self.input_finish_date)
            endpoint = "{}/dpa-api/report".format(self.config['dpa']['host'])
            headers = {
                'Content-Type': 'application/vnd.emc.apollo-v1+xml',
            }
            session = requests.Session()
            session.auth = (self.config['dpa']['username'], self.config['dpa']['password'])
            response = session.post(url=endpoint, headers=headers, data=data, verify=False)
            response.raise_for_status()
            if response.text:
                print(response.headers['Location'])
                return response.headers['Location']
            return None
        except Exception as e:
            raise Exception(e)


    def transform_xml(self, input_xml):
        input_xml = etree.parse(StringIO(input_xml))
        if self.report_name.lower() == 'backup all clients':
            xslt_root = etree.XML('<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"><xsl:output method="xml" version="1.0" encoding="UTF-8" indent="no" /><xsl:template match="/"><DPAJobs><xsl:for-each select="REPORT/EXPRESSION//MULTI"><xsl:variable name="org" select="substring-after(substring-after(INSTANCE[@name=\'Domain Name\']/ITEM/text(), \'/\'), \'/\')"/><xsl:choose><xsl:when test="INSTANCE[@name=\'Backup Application\']/ITEM/text() = \'mssqldb\'"><DPAvm><Client><xsl:value-of select="INSTANCE[@name=\'Client\']/ITEM/text()" disable-output-escaping="no" /></Client><Org><xsl:value-of select="$org" disable-output-escaping="no" /></Org><domainName><xsl:value-of select="concat(\'/\', $org)" disable-output-escaping="no" /></domainName><group><xsl:value-of select="concat($org, \'_SQL_AGENT\')" disable-output-escaping="no" /></group><schedule><xsl:value-of select="concat($org, \'_\', INSTANCE[@name=\'Policy Used\']/ITEM/text())" disable-output-escaping="no" /></schedule><backupServer><xsl:value-of select="INSTANCE[@name=\'Server\']/ITEM/text()" disable-output-escaping="no" /></backupServer><status><xsl:value-of select="INSTANCE[@name=\'Status\']/ITEM/text()" disable-output-escaping="no" /></status> <jobs><xsl:value-of select="INSTANCE[@name=\'Num Jobs\']/ITEM/text()" disable-output-escaping="no" /></jobs></DPAvm></xsl:when><xsl:otherwise><DPAvm><Client><xsl:value-of select="INSTANCE[@name=\'Client\']/ITEM/text()" disable-output-escaping="no" /></Client><Org><xsl:value-of select="$org" disable-output-escaping="no" /></Org><domainName><xsl:value-of select="INSTANCE[@name=\'Domain Name\']/ITEM/text()" disable-output-escaping="no" /></domainName><group><xsl:value-of select="INSTANCE[@name=\'Group\']/ITEM/text()" disable-output-escaping="no" /></group><schedule><xsl:value-of select="INSTANCE[@name=\'Schedule\']/ITEM/text()" disable-output-escaping="no" /></schedule><backupServer><xsl:value-of select="INSTANCE[@name=\'Server\']/ITEM/text()" disable-output-escaping="no" /></backupServer><status><xsl:value-of select="INSTANCE[@name=\'Status\']/ITEM/text()" disable-output-escaping="no" /></status><jobs><xsl:value-of select="INSTANCE[@name=\'Num Jobs\']/ITEM/text()" disable-output-escaping="no" /></jobs></DPAvm></xsl:otherwise></xsl:choose></xsl:for-each></DPAJobs></xsl:template></xsl:stylesheet>')
        if self.report_name.lower() == 'ccb usage report':
            xslt_root = etree.XML('<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"><xsl:output indent="no" /><xsl:template match="/"><dpaclients><xsl:for-each select="REPORT/EXPRESSION//MULTI"><dpaClient><Client><xsl:value-of select="INSTANCE[@name=\'Client\']/ITEM/text()" disable-output-escaping="no" /></Client><FEA><xsl:choose><xsl:when test="contains(INSTANCE[@name=\'Size Scanned\']/ITEM/text(), \'E\')"><xsl:variable name="number" select="substring-before(INSTANCE[@name=\'Data Protected on Client\']/ITEM/text(),\'E\')" /><xsl:variable name="power" select="substring-after(INSTANCE[@name=\'Data Protected on Client\']/ITEM/text(),\'E\')" /><xsl:variable name="powertotal"><xsl:call-template name="power"><xsl:with-param name="base" select="10" /><xsl:with-param name="power" select="$power" /></xsl:call-template></xsl:variable><xsl:value-of select="round(($number * $powertotal) div 1024)" disable-output-escaping="no" /></xsl:when><xsl:otherwise><xsl:value-of select="round(INSTANCE[@name=\'Size Scanned\']/ITEM/text() div 1024)" disable-output-escaping="no" /></xsl:otherwise></xsl:choose></FEA><Org><xsl:value-of select="@name" disable-output-escaping="no" /></Org></dpaClient></xsl:for-each></dpaclients></xsl:template><xsl:template name="power"><xsl:param name="base" /><xsl:param name="power" /><xsl:param name="result" select="1" /><xsl:choose><xsl:when test="number($base) != $base or number($power) != $power"><xsl:value-of select="\'NaN\'" /></xsl:when><xsl:when test="$power = 0"><xsl:value-of select="$result" /></xsl:when><xsl:otherwise><xsl:call-template name="power"><xsl:with-param name="base" select="$base * $base" /><xsl:with-param name="power" select="floor($power div 2)" /><xsl:with-param name="result" select="$result * $base * ($power mod 2) + $result * not($power mod 2)" /></xsl:call-template></xsl:otherwise></xsl:choose></xsl:template></xsl:stylesheet>')
        transform = etree.XSLT(xslt_root)
        result = transform(input_xml)
        return self.transform_xml_to_json(result)

    def transform_xml_to_json(self, xml):
        #tree = etree.parse(xml)
        root = xml.getroot()
        d={}
        for child in root:
            if child.tag not in d:
                d[child.tag]=[]
            dic={}
            for child2 in child:
                if child2.tag not in dic:
                    dic[child2.tag]=child2.text
            d[child.tag].append(dic)
        return d
