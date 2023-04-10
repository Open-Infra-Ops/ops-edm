# -*- coding: utf-8 -*-
import datetime
import yaml
import smtplib
import pandas as pd
from email.header import Header
from email.mime.text import MIMEText


class GlobalConfig:
    title = {
        "overview": "概览",
        "ops_dev": "运维开发",
        "demand_dev": "需求开发",
        "service_change": "社区服务变更",
        "monitor_alarm": "监控告警处理",
        "cost_budget_statistics": "成本预算统计",
        "security_risk_statistics": "安全风险统计",
    }
    excel_template_name = "osinfra_monthly_template.xlsx"
    read_html_template_name = "static/template.html"
    write_html_template_name = "edm.html"
    div_template = '''<div class="table_div">
    <h3 class="h3_title">-------------------------{}-------------------------</h3>
    <br>
    {}
    </div>'''
    edm_config = 'edm.yaml'
    edm_config_fields = [
        "email_server_address",
        "email_server_port",
        "email_login_username",
        "email_login_pwd",
        "email_from_email",
        "email_from_name",
        "email_subject",
        "email_sender_email",
    ]


def parse_yaml():
    with open(GlobalConfig.edm_config, 'r', encoding='utf-8') as f:
        yaml_config = yaml.load(f, Loader=yaml.FullLoader)
    if set(GlobalConfig.edm_config_fields) - set(yaml_config.keys()):
        raise RuntimeError("incorrect configuration in edm.yaml")
    return yaml_config


# noinspection PyShadowingNames
def template_content():
    content, html_dict, html_content = str(), dict(), str()
    pd.set_option('display.width', 1000)
    pd.set_option('colheader_justify', 'center')
    for key, value in GlobalConfig.title.items():
        df = pd.read_excel(GlobalConfig.excel_template_name, sheet_name=key)
        content = df.to_html(index=False, render_links=True, float_format=lambda x: format(x, ',.2f'))
        content = content.replace(r"\n", "")
        html_dict[value] = content
    for key, value in html_dict.items():
        html_content += GlobalConfig.div_template.format(key, value)
    with open(GlobalConfig.read_html_template_name, "r") as f:
        template_content = f.read()
    template_content = template_content.replace(r"{{template}}", html_content)
    with open(GlobalConfig.write_html_template_name, "w") as f:
        f.write(template_content)
    return template_content


def send_email(edm_config, html_msg):
    msg = MIMEText(html_msg, _subtype='html')
    email_subject = "{}_{}".format(edm_config["email_subject"], str(datetime.date.today()))
    msg['Subject'] = Header(email_subject, 'utf-8')
    msg['From'] = Header(edm_config["email_from_email"])
    msg['To'] = Header(",".join(edm_config["email_sender_email"]))
    smtp_handler = smtplib.SMTP_SSL(host=edm_config["email_server_address"],
                                    port=edm_config["email_server_port"])
    smtp_handler.login(edm_config["email_login_username"],
                       edm_config["email_login_pwd"])
    smtp_handler.sendmail(edm_config["email_from_email"],
                          edm_config["email_sender_email"], msg=msg.as_string())


def main():
    print("-----begin-----")
    yaml_config = parse_yaml()
    content = template_content()
    send_email(yaml_config, content)
    print("-----success-----")


if __name__ == '__main__':
    main()
