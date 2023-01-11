import boto3
import time
import json

default_ports = "22,8080,8443,3030,27117"


def init_client():
    # Create a session with the specified AWS access key and secret key
    session = boto3.Session(
        aws_access_key_id='AKIARUGULLAY4R4YGN3G',
        aws_secret_access_key='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',
        region_name='eu-west-3'
    )

    client = session.client('ec2')
    return client


def create_network_insights_path(source, destination,port):
    response_create = client.create_network_insights_path(
        Source=source,
        Destination=destination,
        Protocol='tcp',
        DestinationPort=port
    )
    network_insights_path_id = response_create['NetworkInsightsPath']['NetworkInsightsPathId']
    prints("Network Insight Path Created. NetworkInsightsPathId: " + network_insights_path_id)

    
    return response_create['NetworkInsightsPath']

def start_network_insights_analysis(network_insights_path_id):
    response_start = client.start_network_insights_analysis(
        NetworkInsightsPathId=network_insights_path_id
    )

    analysis_id = response_start['NetworkInsightsAnalysis']['NetworkInsightsAnalysisId']
    prints("Network Analisys Started. NetworkInsightsAnalysisId: " + analysis_id)

    return response_start['NetworkInsightsAnalysis']


def fetch_network_insights_analyses_result(analysis_id):    
    response_describe = None
    status = None
    while True:
        response_describe = client.describe_network_insights_analyses(
            NetworkInsightsAnalysisIds=[
                analysis_id,
            ])
        status = response_describe['NetworkInsightsAnalyses'][0]['Status']
        prints("Waiting for Analysis completion. Status: "  + status)
        time.sleep(5)
        if status != 'running':
            break
    
    full_info = response_describe['NetworkInsightsAnalyses'][0]
    network_path_found = full_info['NetworkPathFound']
    return {
        "status" : status,
        "network_path_found" : network_path_found,
        "info" : full_info
    } 



def get_inputs():
    subnet1 = input("Please enter the source Subnet ID - Subnet1:") 
    subnet2 = input("Please enter the destination Subnet ID - Subnet2:") 
    # analyze_bi_direction = input("Analizy bi-direction (y/n):")
    analyze_specific_ports = input("Analizy specific ports (list comma delimited):")

    if analyze_specific_ports == '':
        analyze_specific_ports = default_ports

    analyze_specific_ports_list = list(analyze_specific_ports.split(","))

    return {
        "subnet1" : subnet1,
        "subnet2" : subnet2,
        "analyze_bi_direction" : False,
        "analyze_specific_ports_list" : analyze_specific_ports_list
    }


def analyze(subnet1_eni, subnet2_eni, analyze_specific_ports_list):

    prints("Start analysis network connectivity of Subnet1 via: " + subnet1_eni + " --> to Subnet2 via " + subnet2_eni + ", on ports: " + str(analyze_specific_ports_list))

    analyzation_result = {
        "full_network_path_found" : True,
        "path_info" : []  
    }
    
    for port in analyze_specific_ports_list:
        analyze_per_port(subnet1_eni, subnet2_eni, analyzation_result, port)
    return analyzation_result

def analyze_per_port(subnet1_eni, subnet2_eni, analyzation_result, port):
    port = int(port)
    prints("Analyzing port: " + str(port))

    create_network_insights_path_response = create_network_insights_path(subnet1_eni, subnet2_eni, port)
    start_network_insights_analysis_resposne = start_network_insights_analysis(create_network_insights_path_response["NetworkInsightsPathId"])
    fetch_network_insights_analyses_result_response = fetch_network_insights_analyses_result(start_network_insights_analysis_resposne["NetworkInsightsAnalysisId"])
    if analyzation_result["full_network_path_found"] != False:
        analyzation_result["full_network_path_found"] = fetch_network_insights_analyses_result_response["network_path_found"]

    path_result = {
            "network_path_found" : fetch_network_insights_analyses_result_response["network_path_found"],
            "source": subnet1_eni,
            "destination": subnet2_eni,
            "port": port
        }
    analyzation_result["path_info"].append(path_result)
    print_header2("Analysis on port: " + str(port) + " completed")

def create_eni(subnet1, eni):
    prints("Creating eni in Subnet: " + subnet1)
    time.sleep(5)
    prints("eni created: " + eni)
    subnet1_eni = eni
    return subnet1_eni

def create_network_endpoints(subnet1,subnet2):
    subnet1_eni = create_eni(subnet1,"eni-07e760710fa0a7d09") #TEMP
    subnet2_eni = create_eni(subnet2,"eni-0d94f19d7a00ed1a5") #TEMP
    return {
        "subnet1_eni" : subnet1_eni,
        "subnet2_eni" : subnet2_eni
    }

def print_header1(text):
    print("")
    print('*********************************************************')
    print('************ ' + text + " ")
    print('*********************************************************')
    print("")
    print("")

def print_header2(text):
    print("")
    print('************ ' + text)
    print("")

def prints(text):
    print(text)


if __name__ == '__main__':
    print_header1("eDSF Sonar Network Analyzer Tool")

    client = init_client()
    
    inputs = get_inputs()

    print_header2("Analysis Started")

    endpoints = create_network_endpoints(inputs["subnet1"],inputs["subnet2"])

    analyzation_list = analyze(
        endpoints["subnet1_eni"],
        endpoints["subnet2_eni"],
        inputs["analyze_specific_ports_list"])


    print (json.dumps(analyzation_list, indent=4, sort_keys=True, default=str))


# Print the details of the path

# # print(response_create)
# print("----------------")
# print("Test: " + status)
# print("Network: " + str(network_path_found))
# print("Details ************")
# # print (json.dumps(response_describe, indent=4, sort_keys=True, default=str))
