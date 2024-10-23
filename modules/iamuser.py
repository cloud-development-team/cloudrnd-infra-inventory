import pandas as pd


def extract_groups(groups):
    group_names = []

    for group in groups:
        group_name = group['GroupName']
        if group_name not in group_names:
            group_names.append(group_name)

    sorted_groups = sorted(group_names)
    return '\n'.join(sorted_groups)


def extract_mfa(mfa_devices):
    for device in mfa_devices:
        if all(key in device for key in ['UserName', 'EnableDate', 'SerialNumber']):
            return 'Enabled'
    return 'Disabled'


def transform_iam_user_data(iamuser_data):
    transformed_data = pd.DataFrame({
        'Name': iamuser_data['name'],
        'IAM Group': iamuser_data['groups'].apply(extract_groups),
        'MFA Device': iamuser_data['mfa_devices'].apply(extract_mfa),
        'Create Date': iamuser_data['create_date'].dt.tz_localize(None),
        'Password Last Used': iamuser_data['password_last_used'].dt.tz_localize(None),
    })

    transformed_data = transformed_data.sort_values(by='Name', ascending=False)

    return transformed_data


def load_and_transform_iam_user_data(iamuser_data):
    return transform_iam_user_data(iamuser_data)
