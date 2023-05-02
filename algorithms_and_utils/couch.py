import requests
import json
import pdb
import pandas as pd
import numpy as np
from collections import defaultdict


class couch_utils:
    def __init__(self, DNS, DB_PORT, IMAGES_DB, DB_ADMIN_USER, DB_ADMIN_PASS, ADMIN_PARTY):
        self.DNS = DNS
        self.DB_PORT = DB_PORT
        self.IMAGES_DB = IMAGES_DB
        self.DB_ADMIN_USER = DB_ADMIN_USER
        self.DB_ADMIN_PASS = DB_ADMIN_PASS
        self.ADMIN_PARTY = ADMIN_PARTY

    def check_if_admin_party_then_make_request(self, url, method="GET", data="no data"):
        """
        Checks if we are in admin party and if so sends necessary credentials
        """
        if method == "GET":
            # pdb.set_trace()
            if self.ADMIN_PARTY:
                response = requests.get('{}'.format(url))
            else:
                response = requests.get('{}'.format(
                    url), auth=(self.DB_ADMIN_USER, self.DB_ADMIN_PASS))
        elif method == "PUT":
            # pdb.set_trace()
            if self.ADMIN_PARTY:
                response = requests.put(url, data=data)
            else:
                response = requests.put(
                    url, data=data, auth=(self.DB_ADMIN_USER, self.DB_ADMIN_PASS))
        elif method == "DELETE":
            # pdb.set_trace()
            if self.ADMIN_PARTY:
                response = requests.delete(url)
            else:
                response = requests.delete(
                    url, auth=(self.DB_ADMIN_USER, self.DB_ADMIN_PASS))
        return response

    def get_images(self, key, json_data=False):
        # csv table like data
        base = "http://{}:{}/{}".format(self.DNS, self.DB_PORT, self.IMAGES_DB)
        # view = f"_design/basic_views/_view/imageSet2ImageId_pull?key=\"{key}\"" # Ikbeom
        if key is None:
            view = f"_design/images/_view/imagesBySet"
        else:
            view = f"_design/images/_view/imagesBySet?key=\"{key}\""
        url = f"{base}/{view}"
        print(url)
        # pdb.set_trace()
        response = self.check_if_admin_party_then_make_request(url)
        results = json.loads(response.content.decode('utf-8'))
        if json_data:
            # raw couchdb results
            Data = results
        else:
            # pdb.set_trace()
            rows = [row["value"] for row in results["rows"]]
            for i in rows:
                # pdb.set_trace()
                del i['_attachments']
            header = rows[0].keys()
            Data = pd.DataFrame(rows, columns=header)

        return Data

    def get_classification_results(self, username, list_name, json_data=False, app=""):
        base = "http://{}:{}/{}".format(self.DNS, self.DB_PORT, self.IMAGES_DB)
        # view = f"_design/basic_views/_view/resultsClassify_userList?key=[\"{username}\", \"{list_name}\"]"
        view = f"_design/basic_views/_view/resultsClassify?key=[\"{username}\", \"{list_name}\"]"
        url = f"{base}/{view}"
        response = self.check_if_admin_party_then_make_request(url)
        results = json.loads(response.content.decode('utf-8'))
        if json_data:
            # raw couchdb results
            Data = results
        elif app == "FGS":
            rows = [row["value"] for row in results["rows"]]
            diagnosis_header = [i for i in rows[0] if i.find(
                'diagnosis_') != -1 or i.find('diagnoisis_') != -1]  # I had a spelling error in the app
            diagnosis_header
            header = ["_id", "_rev", "user", "type", "date", "image"] + \
                diagnosis_header + ["task", "task_list_name", "task_idx"]
            row_data = []
            for row in rows:
                row_values = []
                for col in header:
                    row_values.append(row[col])
                row_data.append(row_values)
            Data = pd.DataFrame(rows, columns=header)
        elif app == "MIDRC":
            Data = pd.DataFrame()
            for row in results["rows"]:
                row_values = row['value']
                row_values_d = {k: [row_values[k]] for k in row_values.keys()}
                # header = list(row_values_d.keys()) + ['reject_justification'] # might not need
                if 'reject_justification' in row['value'].keys():
                    row_values_d['reject_justification'] = [
                        row_values_d['reject_justification']]
                else:
                    row_values_d['reject_justification'] = [np.nan]
                Data = pd.concat([Data, pd.DataFrame(row_values_d)], axis=0)
        else:
            # pdb.set_trace()
            rows = [row["value"] for row in results["rows"]]
            header = [
                "_id",
                "_rev",
                "user",
                "type",
                "date",
                "image",  # if there are errors check if this comes through as image0 not image
                "diagnosis",
                "justification",
                "task",
                "task_list_name",
                "task_idx"]
            Data = pd.DataFrame(rows, columns=header)
        # pdb.set_trace()
        # Data.loc[:,'imageid'] = Data['image'].str.replace(f'http://{self.DNS}:{self.DB_PORT}/{self.IMAGES_DB}/','')

        return Data

    def get_compare_results(self, username, list_name, json_data=False):
        base = "http://{}:{}/{}".format(self.DNS, self.DB_PORT, self.IMAGES_DB)
        view = f"_design/basic_views/_view/resultsCompare?key=[\"{username}\", \"{list_name}\"]"
        url = f"{base}/{view}"
        # pdb.set_trace()
        response = self.check_if_admin_party_then_make_request(url)
        results = json.loads(response.content.decode('utf-8'))
        if json_data:
            # raw couchdb results
            Data = results
            # pdb.set_trace()
        else:
            rows = [row["value"] for row in results["rows"]]
            header = [
                "_id",
                "_rev",
                "user",
                "type",
                "date",
                "image0",
                "image1",
                "winner",
                "justification",
                "task",
                "task_list_name",
                "task_idx"]
            Data = pd.DataFrame(rows, columns=header)
            # pdb.set_trace()
            Data.loc[:, 'image0'] = Data['image0'].str.replace(
                f'http://{self.DNS}:{self.DB_PORT}/{self.IMAGES_DB}/', '')
            Data.loc[:, 'image1'] = Data['image1'].str.replace(
                f'http://{self.DNS}:{self.DB_PORT}/{self.IMAGES_DB}/', '')

        return Data

    def get_frontal_lateral_results(self, username, list_name, json_data=False):
        base = "http://{}:{}/{}".format(self.DNS, self.DB_PORT, self.IMAGES_DB)
        view = f"_design/basic_views/_view/resultsPair?key=[\"{username}\",\"{list_name}\"]"
        url = f"{base}/{view}"
        response = self.check_if_admin_party_then_make_request(url)
        results = json.loads(response.content.decode('utf-8'))
        if json_data:
            # raw couchdb results
            Data = results
            pdb.set_trace()
        else:
            rows = [row["value"] for row in results["rows"]]
            # for row in rows:
            #     pdb.set_trace()
            #     if row
            header = [
                "_id",
                "_rev",
                "user",
                "type",
                "date",
                "image0",
                "image1",
                "classification0",
                "classification1",
                "accept_or_reject",
                "reject_justification",
                "optional_comment",
                "task"
                "task_list_name",
                "task_idx"
            ]
            # pdb.set_trace()
            Data = pd.DataFrame(rows, columns=header)
            # pdb.set_trace()
            Data.loc[:, 'image0'] = Data['image0'].str.replace(
                f'http://{self.DNS}:{self.DB_PORT}/{self.IMAGES_DB}/', '')
            Data.loc[:, 'image1'] = Data['image1'].str.replace(
                f'http://{self.DNS}:{self.DB_PORT}/{self.IMAGES_DB}/', '')

        return Data

    def get_grid_results(self, username, list_name, json_data=False, app=""):
        base = "http://{}:{}/{}".format(self.DNS, self.DB_PORT, self.IMAGES_DB)
        view = f"_design/basic_views/_view/resultsGrid?key=[\"{username}\",\"{list_name}\"]"
        url = f"{base}/{view}"
        response = self.check_if_admin_party_then_make_request(url)
        results = json.loads(response.content.decode('utf-8'))
        # data
        rows = [row["value"] for row in results["rows"]]
        images = rows[0]['couch_results'].keys()
        class_results = rows[0]['couch_results'].values()
        task_list_name = [rows[0]['task_list_name']
                          for i in range(len(rows[0]['couch_results'].keys()))]
        user = [rows[0]['user']
                for i in range(len(rows[0]['couch_results'].keys()))]
        if json_data:
            # raw couchdb results
            Data = results
            pdb.set_trace()
        elif app == "MIDRC":
            header_addon = list(list(class_results)[0].keys())
            results = defaultdict(list)
            for result_set in class_results:
                for col in header_addon:
                    results[col].append(result_set[col])
            results_lists = []
            for i in results.keys():
                results_lists.append(results[i])
            header = [
                "user",
                "image",
                "task_list_name"] + header_addon
            # pdb.set_trace()
            Data = pd.DataFrame(
                zip(user, images, task_list_name, *results_lists), columns=header)
            # pdb.set_trace()
            Data.rename(
                columns={'image_name': 'SOPInstanceUID_png'}, inplace=True)
        else:
            header = [
                "user",
                "image",
                "class",
                "task_list_name"]
            Data = pd.DataFrame(
                zip(user, images, class_results, task_list_name), columns=header)
            # pdb.set_trace()
            Data.loc[:, 'image'] = Data['image'].str.replace('image_', '')

        return Data

    def get_flicker_results(self, username, list_name, json_data=False, app=""):
        base = "http://{}:{}/{}".format(self.DNS, self.DB_PORT, self.IMAGES_DB)
        # view = f"_design/basic_views/_view/resultsClassify_userList?key=[\"{username}\", \"{list_name}\"]"
        view = f"_design/flickerApp/_view/results?key=[\"{username}\", \"{list_name}\"]"
        url = f"{base}/{view}"
        response = self.check_if_admin_party_then_make_request(url)
        results = json.loads(response.content.decode('utf-8'))
        base_header = ['user','app','list_name','taskid']
        results_df = pd.DataFrame()
        for row in results['rows']:
            # pdb.set_trace()
            if row['value']['radio_button_categories']:
                radio_button_results = []
                for radio_button in row['value']['radio_button_categories']:
                    if radio_button['category_id'] not in base_header:
                        base_header.append(radio_button['category_id'])
                    radio_button_results.append((radio_button['category_id'], radio_button['selected']))
            if row['value']['slider_input_categories']:
                slider_button_results = []
                for slider_input in row['value']['slider_input_categories']:
                    for image_opacity in slider_input['slider_inputs']:
                        if image_opacity['slider_input_id'] not in base_header:
                            base_header.append(image_opacity['slider_input_id'])
                        slider_button_results.append((image_opacity['slider_input_id'], image_opacity['value']))
            row_results = radio_button_results + slider_button_results
            row_results_dict = {k:v for k,v in row_results}
            row_dict = {'user':[row['value']['user']],
                        'app':[row['value']['app']],
                        'taskid':[row['value']['taskid']],
                        'list_name':[row['value']['list_name']],
                        '_id':[row['value']['_id']],
                        }
            for result_key in row_results_dict.keys():
                row_dict[result_key] = [row_results_dict[result_key]]
            row_df = pd.DataFrame(row_dict)
            results_df = pd.concat([results_df, row_df])
        # pdb.set_trace()
        return results_df
        

    def get_view(self, view, json_data=False):
        base = "http://{}:{}/{}".format(self.DNS, self.DB_PORT, self.IMAGES_DB)
        view = f"_design/basic_views/_view/{view}"
        url = f"{base}/{view}"
        response = self.check_if_admin_party_then_make_request(url)
        results = json.loads(response.content.decode('utf-8'))
        if json_data:
            # raw couchdb results
            Data = results
            # pdb.set_trace()
        else:
            image_list = results['rows'][0]['value']['list']
            count = results['rows'][0]['value']['count']
            type = results['rows'][0]['value']['type']
            # pdb.set_trace()
            Data = {'list': image_list, 'count': count, 'type': type}

        return Data

    def get_list(self, list_name, json_data=False):
        base = "http://{}:{}/{}".format(self.DNS, self.DB_PORT, self.IMAGES_DB)
        view = f"_design/basic_views/_view/image_compare_lists?key=\"{list_name}\""
        url = f"{base}/{view}"
        response = self.check_if_admin_party_then_make_request(url)
        results = json.loads(response.content.decode('utf-8'))
        # pdb.set_trace()
        if json_data:
            # raw couchdb results
            Data = results
            # pdb.set_trace()
        else:
            image_list = results['rows'][0]['value']['list']
            count = results['rows'][0]['value']['count']
            type = results['rows'][0]['value']['type']
            # pdb.set_trace()
            Data = {'list': image_list, 'count': count, 'type': type}

        return Data
