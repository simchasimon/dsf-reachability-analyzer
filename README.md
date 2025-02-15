<div class="markdown prose w-full break-words dark:prose-invert light">
   <h1>DSF Reachability Analysis Tool</h1>
   <p>This is a tool that allows users to analyze network connectivity between two subnets in an Amazon VPC. The tool uses the AWS EC2 Network Insights feature to create a path between the source and destination subnets and analyzes the connectivity on specified ports.</p>
   <h2>Prerequisites</h2>
   <ul>
      <li>AWS Access Key and Secret Key with permissions to use EC2 Network Insights</li>
      <li>Python 3 and the boto3 library installed</li>
      <li>The source and destination subnet IDs</li>
   </ul>
   <h2>Usage</h2>
   <ol>
      <li>Run the script by entering the command <code>python main.py</code> in the command prompt and answer the questions.</li>
      <li>When asked to, enter a list of ports to analyze connectivity on, comma separated (e.g. "22,8080,8443"). If left blank, the script will use a default list of ports (22,8080,8443,3030,27117) which are all the ports needed for a functional Sonar environment.</li>
   </ol>
   <p>
         **Note**: The script creates and deletes temporary Elastic Network Interfaces (ENIs) in order to perform the analysis. In case of failure, these ENIs may need to be deleted manually.
   </p>
    <h2>AWS IAM Roles</h2>
    <p>
    [See minimum Policy needed](https://github.com/imperva/dsf-reachability-analyzer/blob/master/iam_role.yml)
    </p>
    <h2>Results</h2>
   <p>On Analysis completion the results can be viewd in 3 places:
   <ol>
      <li>On the terminal you will be ablr to see the basic info</li>
       <li>A file will be generated tom include all the analysis including detail info</li>
       <li>On the terminal you will see direct links to AWS Network Analyzer service. The links will bring you directly to the specific analysis. Note that you need to be logged in to the correspondant AWS account</li>
   </ol>
   </p>
   <h2>Additional note</h2>
   <p>It is recommended to use environment variable to manage the aws key and secret key or better using IAM to grant access to your AWS resource, instead of hardcoding them in the script</p>
</div>
