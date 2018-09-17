import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup as bs
import pandas as pd

# make a loop that scans the site peak after peak
# based on webpage serial number
print('Ready, set, go...')
Peak_df = pd.DataFrame(data={})
for peak_num in range(1,5000):
    peak_data_dict={} # initialising temp data dict
    peak_url = 'https://www.peakware.com/peaks.php?pk={}'.format(peak_num)
    # Get site text
    with urllib.request.urlopen(peak_url) as f:
        site_text=(f.read().decode('utf-8','ignore'))
    # print('peak number', peak_num)
    soup = bs(site_text, 'lxml')  # compare with 'html'
    # tag.find_all(name, attrs, recursive, text, limit)
    peak_name_tags = soup.find(name='h1')
    peak_name = peak_name_tags.get_text()
    # exit loop when no more peaks
    if peak_name == 'Peak Not Found':
        pass
    else:
        print(peak_num, peak_name)#, end=' ')
        # building a dict with peak's data
        df = pd.read_html(peak_url)
        peak_sample = pd.DataFrame(df[0])
        for index in range(len(peak_sample)):
            k,v=peak_sample.iloc[index]
            peak_data_dict[k]=[v]
        # add peak name to peak data dict
        Peak_data = pd.DataFrame(data=peak_data_dict, index=[peak_name])
        Peak_df=pd.concat([Peak_df, Peak_data])
# Save DataFrame to a file for future use
Peak_df.to_csv('Peak_temp_db.csv')
print('Finished')