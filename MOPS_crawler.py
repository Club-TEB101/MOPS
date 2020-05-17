from collections import OrderedDict

import requests
import pandas as pd
from bs4 import BeautifulSoup


class HTMLTableParser:

    def get_html_tables_from_resp(self, html_text):
        soup = BeautifulSoup(html_text, 'html.parser')
        tables = soup.find_all('table')
        return tables

    def parse_html_table(self, table):
        """
        <tr>
            <th align="center" class="tblHead" nowrap="" rowspan="2">產業類別</th>
            <th align="center" class="tblHead" nowrap="" rowspan="2">公司代號</th>
            <th align="center" class="tblHead" nowrap="" rowspan="2">公司名稱</th>
            <th align="center" class="tblHead" colspan="4" nowrap="">非擔任主管職務之<br/>全時員工資訊</th>
            <th align="center" class="tblHead" colspan="2" nowrap="">同業公司資訊</th>
            <th align="center" class="tblHead" colspan="4" nowrap="">薪資統計情形</th>
        </tr>
        <tr>
            <th align="center" class="tblHead" nowrap="">員工薪資總額(仟元)</th>
            <th align="center" class="tblHead" nowrap="">員工人數-加權平均(人)</th>
            <th align="center" class="tblHead" nowrap="">員工薪資-平均數(仟元/人)</th>
            <th align="center" class="tblHead" nowrap="">每股盈餘(元/股)</th>
            <th align="center" class="tblHead" nowrap="">員工薪資-平均數(仟元/人)</th>
            <th align="center" class="tblHead" nowrap="">平均每股盈餘(元/股)</th>
            <th align="center" class="tblHead" nowrap="">非經理人之<br/>全時員工薪資<br/>平均數未達50萬元</th>
            <th align="center" class="tblHead" nowrap="">公司EPS獲利表現較同業為佳<br/>，惟非經理人之全時員工<br/>薪資平均數低於同業水準</th>
            <th align="center" class="tblHead" nowrap="">公司EPS較前一年度成長<br/>，惟非經理人之全時員工<br/>薪資平均數較前一年度減少</th>
            <th align="center" class="tblHead" nowrap="">公司經營績效與員工薪酬<br/>之關聯性及合理性說明</th>
        </tr>
        <tr>
            <td nowrap="" style="text-align:left !important;">資訊服務業</td>
            <td nowrap="" style="text-align:left !important;">8416</td>
            <td nowrap="" style="text-align:left !important;">實威</td>
            <td nowrap="" style="text-align:right !important;"> 158,636 </td>
            <td nowrap="" style="text-align:right !important;"> 186 </td>
            <td nowrap="" style="text-align:right !important;"> 853 </td>
            <td nowrap="" style="text-align:right !important;"> 9.69 </td>
            <td nowrap="" style="text-align:right !important;"> 807 </td>
            <td nowrap="" style="text-align:right !important;"> 1.20 </td>
            <td nowrap="" style="text-align:right !important;"></td>
            <td nowrap="" style="text-align:right !important;"></td>
            <td nowrap="" style="text-align:right !important;"></td>
            <td nowrap="" style="text-align:left !important;"><br/></td>
        </tr>
        """
        parsed_data = []

        # Find number of rows and columns
        # we also find the column titles if we can
        table_row_tags = table.find_all('tr')
        table_header_tags = table.find_all('th')
        column_names = [table_header_tag.get_text() for key, table_header_tag in enumerate(table_header_tags) if key not in (3, 4, 5)]
        column_names[7] = '同業公司{}'.format(column_names[7])
        column_names[8] = '同業公司{}'.format(column_names[8])

        tr_td_tags = [
            [td_tag.get_text().strip() for td_tag in table_row.find_all('td')]
            for table_row in table_row_tags if table_row.find_all('td')
        ]

        parsed_data = [
            OrderedDict({
                column_names[index]: td_tag
                for index, td_tag in enumerate(tr_td_tag)
            })
            for tr_td_tag in tr_td_tags
        ]

        df = pd.DataFrame.from_dict(parsed_data)

        return df


htlm_parser = HTMLTableParser()

payload = {
    # 'encodeURIComponent': 1,
    'step': 1,
    'firstin': 1,
    'TYPEK': 'sii', # sii 上市 / otc 上櫃
    'RYEAR': 107,
    'code': '',
}

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

resp = requests.post('https://mops.twse.com.tw/mops/web/ajax_t100sb15', data=payload, headers=headers, timeout=2)

html_tables = htlm_parser.get_html_tables_from_resp(resp.text)

df_table = htlm_parser.parse_html_table(html_tables[0])

df_table.to_csv('107_{}.csv'.format(payload['TYPEK']), index=False, encoding='utf-8')

print(df_table)
