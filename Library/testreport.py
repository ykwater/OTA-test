import webbrowser
import re
from path import TESTREPORT_PATH



endtime = 1
casenamber = 2
casetitle = 3
casedescribe = 4
taskid = 5
result = "PASS"
failurestatus = None

html_head = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <style>
    table tr td {border: 1px solid #e4e4e4;}
    </style>
    </head>\n
    """

html_script = """
    </body> 
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.3.2/dist/echarts.min.js"></script>
    <script>
        var myChart = echarts.init(document.getElementById('chart'))
        // 指定图表的配置项和数据
        var option = {
            title: {
                text: '测试情况饼图统计',
                left: 'center',
            },
            tooltip: {
                trigger: 'item',
            },
            legend: {
                orient: 'vertical',
                left: 'left',
            },
            series: [
                {
                    name: '测试情况饼图统计',
                    type: 'pie',
                    radius: '70%', //这个属性调整图像的大小
                    center: ['60%', '60%'], //这个属性调整图像的位置
                    data: [
                        { value: %s, name: '用例成功' },
                        { value: %s, name: '用例跳过' },
                        { value: %s, name: '用例失败' },
                    ],
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)',
                        },
                    },
                },
            ],
            color: ["green", "rgb(255, 196, 0)", "red"]
        }

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option)
    </script>
    </html>
    """


class reporthtml(object):
    def pass_html(self, i,id,title,describe,s_time,t_time):
        html_list = f"""
                        <tr>
                            <td>{str(i)}</td>
                            <td>{id}</td>
                            <td>{title}</td>
                            <td>{describe}</td>
                            <td>{s_time}</td>
                            <td>{t_time}</td>
                            <td style="color: green; font-weight:bold">PASS</td>
                            <td> </td>
                        </tr>\n
                        """
        return html_list

    def fail_html(self, i,id,title,describe,s_time,t_time,result):
        html_list = f"""
                        <tr>
                            <td>{str(i)}</td>
                            <td>{id}</td>
                            <td>{title}</td>
                            <td>{describe}</td>
                            <td>{s_time}</td>
                            <td>{t_time}</td>
                            <td style="color: red; font-weight:bold">FAIL</td>
                            <td>{result}</td>
                        </tr>\n
                        """
        return html_list

    def smoke_test(self,passd, fail, abc, starttime, endtime):
        html_body = f"""
        <body>
        <table width="100%;" cellspacing="0">
            <tr>
                <td>
                    <h1 align="center" style="color: green; text-align: center">测试报告</h1>
                </td>
            </tr>
        </table>
        <table width="100%;" cellspacing="0">
            <tr>
                <td>
                    <h2>&nbsp; 报告汇总</h2>
                </td>
            </tr>
        </table>
        <table width="100%"; cellspacing="0">
            <tr>
                <td>
                    <table width="400"; cellspacing="30" >
                        <tr>
                            <td width="100"; style="color: green; font-weight:bold">用例通过: </td>
                            <td width="300">{passd}</td>
                        </tr>
                        <tr>
                            <td width="100"; style="color: red; font-weight:bold">用例失败: </td>
                            <td width="300">{fail}</td>
                        </tr>

                        <tr>
                            <td width="100"; style="color: black; font-weight:bold">用例总数: </td>
                            <td width="300">{passd + fail}</td>
                        </tr> 
                        <tr>
                            <td width="100"; style="color: black; font-weight:bold">开始时间: </td>
                            <td width="300">{starttime}</td>
                        </tr>
                        <tr>
                            <td width="100"; style="color: black; font-weight:bold">结束时间: </td>
                            <td width="300">{endtime}</td>
                        </tr>
                    </table>
                </td>
                <td>
                    <div id="chart" style="width: 500px; height: 400px;"></div>
                </td>
            </tr>
        </table>  
        <table width="100%;" cellspacing="0">
            <tr>
                <td>
                    <h2>&nbsp; 测试详情</h2>
                </td>
            </tr>
        </table>
        <table width="100%"; cellspacing="0">
            <tr style="font-weight:bold"; bgcolor="#C0C0C0">
                <td width="50">编号</td>
                <td width="70">任务ID</td>
                <td width="220">用例标题</td>
                <td>用例描述</td>
                <td width="200">开始时间</td>
                <td width="200">结束时间</td>
                <td width="70">结果</td>
                <td >失败原因</td>
            </tr>\n
        """
        script_path = f"""
            </body> 
            <script src="https://cdn.jsdelivr.net/npm/echarts@5.3.2/dist/echarts.min.js"></script>\n
        """
        html_script = """
            <script>
                var myChart = echarts.init(document.getElementById('chart'))
                // 指定图表的配置项和数据
                var option = {
                    title: {
                        text: '测试情况饼图统计',
                        left: 'center',
                    },
                    tooltip: {
                        trigger: 'item',
                    },
                    legend: {
                        orient: 'vertical',
                        left: 'left',
                    },
                    series: [
                        {
                            name: '测试情况饼图统计',
                            type: 'pie',
                            radius: '60%', //这个属性调整图像的大小
                            center: ['60%', '60%'], //这个属性调整图像的位置
                            data: [
                                { value: 成功的次数, name: '用例成功' },
                                { value: 0, name: '用例跳过' },
                                { value: 失败的次数, name: '用例失败' },
                            ],
                            emphasis: {
                                itemStyle: {
                                    shadowBlur: 10,
                                    shadowOffsetX: 0,
                                    shadowColor: 'rgba(0, 0, 0, 0.5)',
                                },
                            },
                        },
                    ],
                    color: ["green", "rgb(255, 196, 0)", "red"]
                }

                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option)
            </script>
        </html>
        """
        html_script = re.sub("成功的次数", f"{passd}", html_script, count=1)
        html_script = re.sub("失败的次数", f"{fail}", html_script, count=1)
        caa = html_head + html_body + abc + script_path + html_script
        GEN_HTML = rf"{TESTREPORT_PATH}\OTA_Test_Report.html"
        f = open(GEN_HTML, 'w', encoding="utf-8")
        f.write(caa)
        # 关闭文件
        f.close()
        # 运行完自动在网页中显示
        webbrowser.open(GEN_HTML, new=1)

reprot = reporthtml()
if __name__ == '__main__':
    main_html = ""
    main_html =main_html + reprot.fail_html("1","2","3","4","5","6","7")
    main_html = main_html + reprot.pass_html("1", "2", "3", "4", "5", "6")
    reprot.smoke_test("1","2",main_html,"4","5")