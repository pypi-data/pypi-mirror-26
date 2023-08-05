

export function query(formData, queryResponse) {
  const vizT = ['echarts_bar', 'echarts_bar_waterfall', 'echarts_bar_h', 'echarts_area_stack',
    'echarts_line_bar', 'echarts_line', 'echarts_pie_m', 'echarts_pie_h', 'echarts_pie_g',
    'echarts_multiple_ring_diagram', 'echarts_dash_board', 'echarts_big_number_compare', 'echarts_treemap',
    'echarts_big_number', 'big_number_viz', 'echarts_radar_map', 'echarts_pie_h_g', 'pivot_table', 'table']
  // console.info(formData)
  // 返回的数据用data.d获取内容
  if (vizT.indexOf(formData.viz_type) != -1) {
    const data = queryResponse
    let keys = Object.keys(formData)
    keys.forEach(function (key, index) {
      if (key.indexOf('groupby') >= 0) {
        let group = []
        for (let mf in formData[key]) {
          for (let dg in data.groupby) {
            if (formData[key][mf] == data.groupby[dg][0]) {
              group.push(data.groupby[dg][1])
            }
          }
        }
        if (group.length != 0) {
          formData[key] = group
        }
      }
      //zhexianzhuzhuangtu
      if (key == 'line_choice') {
        if (formData[key] != ('' || null)) {
          let choice = []
          for (let mf in formData[key]) {
            for (let dm in data.metrics) {
              if (formData[key][mf] == data.metrics[dm][0]) {
                choice.push(data.metrics[dm][1])
              }
            }
          }
          if (choice.length != 0) {
            formData.line_choice = choice
          }
        }
      }
      //echarts bubble
      if (key == 'size') {
        if (formData[key] != ('' || null)) {
          let ci = ''
          for (let mf in formData[key]) {
            for (let dm in data.metrics) {
              if (formData[key] == data.metrics[dm][0]) {
                ci = data.metrics[dm][1]
              }
            }
          }
          if (ci != '') {
            formData.size = ci
          }
        }
      }
      if (key == 'x') {
        if (formData[key] != ('' || null)) {
          let ci = ''
          for (let mf in formData[key]) {
            for (let dm in data.metrics) {
              if (formData[key] == data.metrics[dm][0]) {
                ci = data.metrics[dm][1]
              }
            }
          }
          if (ci != '') {
            formData.x = ci
          }
        }
      }
      if (key == 'y') {
        if (formData[key] != ('' || null)) {
          let ci = ''
          for (let mf in formData[key]) {
            for (let dm in data.metrics) {
              if (formData[key] == data.metrics[dm][0]) {
                ci = data.metrics[dm][1]
              }
            }
          }
          if (ci != '') {
            formData.y = ci
          }
        }
      }
      //treemap
      if (key == 'child_id') {
        if (formData[key] != ('' || null)) {
          let ci = ''
          for (let mf in formData[key]) {
            for (let dm in data.groupby) {
              if (formData[key] == data.groupby[dm][0]) {
                ci = data.groupby[dm][1]
              }
            }
          }
          if (ci != '') {
            formData.child_id = ci
          }
        }
      }
      if (key == 'child_name') {
        if (formData[key] != ('' || null)) {
          let cn = ''
          for (let mf in formData[key]) {
            for (let dm in data.groupby) {
              if (formData[key] == data.groupby[dm][0]) {
                cn = data.groupby[dm][1]
              }
            }
          }
          if (cn != '') {
            formData.child_name = cn
          }
        }
      }
      if (key == 'stacks') {
        let stacks = ''
        let st = formData[key]
        if (st.length != 0) {
          for (let s in st) {
            console.info(st[s].metrics)
            let metrics = st[s].metrics.split(',')
            for (let mec in metrics) {
              for (let dm in data.metrics) {
                if (metrics[mec] == data.metrics[dm][0]) {
                  let pi = data.metrics[dm][1]
                  if (metrics[mec] != metrics[metrics.length - 1]) {
                    stacks = stacks + pi + ','
                  }
                  if (metrics[mec] == metrics[metrics.length - 1]) {
                    stacks = stacks + pi
                  }
                }
              }
            }
            if (stacks != '') {
              st[s].metrics = stacks
            }
          }

        }

      }
      if (key == 'parent_id') {
        if (formData[key] != ('' || null)) {
          let pi = ''
          for (let mf in formData[key]) {
            for (let dm in data.groupby) {
              if (formData[key] == data.groupby[dm][0]) {
                pi = data.groupby[dm][1]
              }
            }
          }
          if (pi != '') {
            formData.parent_id = pi
          }
        }
      }
      //echarts_p_h
      if (key == 'inner_metrics_one') {
        if (formData[key] != ('' || null)) {
          let imo = ''
          for (let mf in formData[key]) {
            for (let dm in data.groupby) {
              if (formData[key] == data.groupby[dm][0]) {
                imo = data.groupby[dm][1]
              }
            }
          }
          if (imo != '') {
            formData.inner_metrics_one = imo
          }
        }
      }
      if (key == 'outer_metrics_one') {
        if (formData[key] != ('' || null)) {
          let imo = ''
          for (let mf in formData[key]) {
            for (let dm in data.groupby) {
              if (formData[key] == data.groupby[dm][0]) {
                imo = data.groupby[dm][1]
              }
            }
          }
          if (imo != '') {
            formData.outer_metrics_one = imo
          }
        }
      }
      if (key.indexOf('metric') >= 0) {
        if (formData[key] != ('' || null)) {
          if (typeof (formData[key]) == 'object') {
            let metric = []
            for (let mf in formData[key]) {
              for (let dm in data.metrics) {
                if (formData[key][mf] == data.metrics[dm][0]) {
                  metric.push(data.metrics[dm][1])
                }
              }
            }

            if (metric.length != 0) {
              formData[key] = metric
            }

          }
          if (typeof (formData[key]) == 'string') {
            let metric = ''
            for (let dm in data.metrics) {
              if (formData[key] == data.metrics[dm][0]) {
                metric = data.metrics[dm][1]
              }
            }
            if (metric != '') {
              formData[key] = metric
            }
          }
        }
      }
    });
    console.info(formData)
    return formData
  }
  else {
    return formData
  }
}
