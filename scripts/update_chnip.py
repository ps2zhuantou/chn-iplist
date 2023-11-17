import netaddr
import requests
import logging
import math

#update chnroute-ipv6
logger = logging.getLogger(__name__)


def update_ip():
    url = 'https://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
    timeout = 30
    save_to_file6 = './chnroute-ipv6.txt'


    logger.info(f'connecting to {url}')

    ipNetwork_list6 = []

    with requests.get(url, timeout=timeout) as res:
        if res.status_code != 200:
            raise Exception(f'status code :{res.status_code}')

        logger.info(f'parsing...')

        lines = res.text.splitlines()
        for line in lines:
            try:
                if line.find('|CN|ipv6|') != -1:
                    elems = line.split('|')
                    ip_start = elems[3]
                    cidr_prefix_length = elems[4]
                    ipNetwork_list6.append(netaddr.IPNetwork(f'{ip_start}/{cidr_prefix_length}\n'))
            except IndexError:
                logging.warning(f'unexpected format: {line}')

    logger.info('merging')
    ipNetwork_list6 = netaddr.cidr_merge(ipNetwork_list6)
    logger.info('writing to file')

    with open(save_to_file6, 'wt') as f:
        f.writelines([f'{x}\n' for x in ipNetwork_list6])

    logger.info('all done')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    update_ip()


#update chroute-ipv4
url = "https://raw.githubusercontent.com/PaPerseller/someip/build/cidr.txt"

response = requests.get(url)

if response.status_code == 200:
    with open("chnroute-ipv4.txt", "wb") as file:
        file.write(response.content)
else:
    print(f"文件下载失败，状态码: {response.status_code}")

#update chnroute
with open("./chnroute-ipv4.txt", 'r') as a_file:
    a_content = a_file.read()

with open("./chnroute-ipv6.txt", 'r') as b_file:
    b_content = b_file.read()

merged_content = a_content + b_content

with open('./chnroute.txt', 'w') as output_file:
        output_file.write(merged_content)
