# get_cve_details.py

import requests
import time

from st2common.runners.base_action import Action

class GetCVEDetailsAction(Action):
    def run(self, cve_list):
        cve_details = []

        for cve_obj in cve_list:
            cve_id = cve_obj.get("cve")
            details = self.get_cve_details(cve_id)
            cve_details.append(details)
            time.sleep(12)

        return cve_details

    def get_cve_details(self, cve_id):
      # Define the NIST CVE API URL with the provided CVE ID
      api_url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"

      # Make the API request
      response = requests.get(api_url)

      if response.status_code == 200:
          data = response.json()
          cve = data.get("vulnerabilities", [])[0]

          if cve:
              filtered_cve = {
                  "id": cve["cve"]["id"],
                  "description": cve["cve"]["descriptions"][0]["value"] if "descriptions" in cve["cve"] and cve["cve"]["descriptions"] else "",
                  "tags": cve["cve"]["references"][0]["tags"] if "references" in cve["cve"] and cve["cve"]["references"] and cve["cve"]["references"][0].get("tags") else "",
                  "ref_url": cve["cve"]["references"][0]["url"] if "references" in cve["cve"] and cve["cve"]["references"] else "",
                  "ref_name": cve["cve"]["references"][0]["url"] if "references" in cve["cve"] and cve["cve"]["references"] else "",
                  "ref_source": cve["cve"]["references"][0]["source"] if "references" in cve["cve"] and cve["cve"]["references"] else "",
                  "publishedDate": cve["cve"]["published"],
                  "lastModifiedDate": cve["cve"]["lastModified"],
              }
            
              # Check for the existence of the "references" field and get the tags as a list
              tags = cve["cve"]["references"][0].get("tags", [])

              # Join the tags list into a single string separated by '|'
              tags_string = " | ".join(tags) if tags else ""

              # Assign the tags string to the filtered_cve dictionary
              filtered_cve["tags"] = tags_string


              # Check for different field names for CVSS
              cvss_data = None
              if "cvssMetricV31" in cve["cve"]["metrics"]:
                  cvss_data = cve["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]
                  if cvss_data:
                      filtered_cve.update({
                      "impactVectorString": cvss_data.get("vectorString",""),
                      "impactAttackVector": cvss_data.get("attackVector",""),
                      "impactAttackComplexity": cvss_data.get("attackComplexity",""),
                      "impactPrivilegedRequired": cvss_data.get("privilegesRequired",""),
                      "impactUserInteraction": cvss_data.get("userInteraction",""),
                      "impactScope": cvss_data.get("scope",""),
                      "impactConfidentialityImpact": cvss_data.get("confidentialityImpact",""),
                      "impactIntegrityImpact": cvss_data.get("integrityImpact",""),
                      "impactAvailabilityImpact": cvss_data.get("availabilityImpact",""),
                      "impactBaseScore": cvss_data.get("baseScore",""),
                      "impactBaseSeverity": cvss_data.get("baseSeverity")
                    
                  })
                    
              elif "cvssMetricV3" in cve["cve"]["metrics"]:
                  cvss_data = cve["cve"]["metrics"]["cvssMetricV3"][0]["cvssData"]
                  if cvss_data:
                      filtered_cve.update({
                      "impactVectorString": cvss_data.get("vectorString",""),
                      "impactAttackVector": cvss_data.get("attackVector",""),
                      "impactAttackComplexity": cvss_data.get("attackComplexity",""),
                      "impactPrivilegedRequired": cvss_data.get("privilegesRequired",""),
                      "impactUserInteraction": cvss_data.get("userInteraction",""),
                      "impactScope": cvss_data.get("scope",""),
                      "impactConfidentialityImpact": cvss_data.get("confidentialityImpact",""),
                      "impactIntegrityImpact": cvss_data.get("integrityImpact",""),
                      "impactAvailabilityImpact": cvss_data.get("availabilityImpact",""),
                      "impactBaseScore": cvss_data.get("baseScore",""),
                      "impactBaseSeverity": cvss_data.get("baseSeverity")
                    
                  })
            

              elif "cvssMetricV2" in cve["cve"]["metrics"]:
                  baseSeverity = cve["cve"]["metrics"]["cvssMetricV2"][0]
                  cvss_data = cve["cve"]["metrics"]["cvssMetricV2"][0]["cvssData"]
                  if cvss_data:
                      filtered_cve.update({
                      "impactVectorString": cvss_data.get("vectorString",""),
                      "impactAttackVector": cvss_data.get("accessVector",""),
                      "impactAttackComplexity": cvss_data.get("accessComplexity",""),
                      "impactPrivilegedRequired": cvss_data.get("privilegesRequired",""),
                      "impactUserInteraction": cvss_data.get("userInteraction",""),
                      "impactScope": cvss_data.get("scope",""),
                      "impactConfidentialityImpact": cvss_data.get("confidentialityImpact",""),
                      "impactIntegrityImpact": cvss_data.get("integrityImpact",""),
                      "impactAvailabilityImpact": cvss_data.get("availabilityImpact",""),
                      "impactBaseScore": cvss_data.get("baseScore",""),
                      "impactBaseSeverity": baseSeverity.get("baseSeverity","")
                
                  })
              filtered_cve["impactBaseScore"] = str(cve["cve"]["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"])


              return filtered_cve
          else:
              return {"error": "CVE ID not found"}

      else:
          return {"error": f"Failed to retrieve data for CVE ID {cve_id}. Status code: {response.status_code}"}           


