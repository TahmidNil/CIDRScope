CIDRScope

CIDRScope is a versatile command-line tool designed to help penetration testers and security researchers resolve subdomains and filter them based on given CIDR IP ranges. It allows you to easily manage IP ranges and subdomains, perform resolution, and check if the resolved IPs fall within specified CIDR ranges.
Features

    CIDR Range Input: Allows you to either manually input CIDR ranges or load them from a file.
    Subdomain Resolution: Resolves subdomains using dnsprobe or nslookup and outputs associated IP addresses.
    In-Scope Filtering: Filters resolved IPs to only show those that fall within the provided CIDR ranges.
    Output Options: Option to output results to a file and/or display them on the terminal.
    Debug Mode: Includes detailed debug information to help troubleshoot and understand the tool's operation.

Installation
Prerequisites

    Python 3.6 or higher
    dnsprobe installed : 
    GO111MODULE=on go get -v github.com/projectdiscovery/dnsprobe

You can install the required Python dependencies using pip:
```
pip install -r requirements.txt
```
Clone the Repository

Clone the CIDRScope repository to your local machine:
```
git clone https://github.com/yourusername/CIDRScope.git
cd CIDRScope
```
Usage
Basic Command

```
python cidr_scope.py
```
Options

    -h, --help : Show the help message and available options.
    -o <output_file> : Specify a file to output the results.
    -i : Option to input CIDR ranges manually.
    -f <cidr_file> : Load CIDR ranges from a file.
    -s <subdomain_file> : Load subdomains from a file.

Example

  1. Resolve subdomains and filter in-scope IPs:
```
python cidr_scope.py -f range.txt -s subdomains.txt
```
 2. Save the result to a file and view output on terminal:
```
python cidr_scope.py -f range.txt -s subdomains.txt -o results.txt
```
 3. Manually input CIDR ranges:
```
python cidr_scope.py -i -s subdomains.txt
```
Contributing

We welcome contributions! Please fork the repository, create a new branch, and submit a pull request for any changes or improvements.
