import React from 'react';
import PropTypes from 'prop-types';
import { ButtonGroup } from 'react-bootstrap';

import Button from '../../components/Button';
import CssEditor from './CssEditor';
import RefreshIntervalModal from './RefreshIntervalModal';
import SaveModal from './SaveModal';
import CodeModal from './CodeModal';
import SliceAdder from './SliceAdder';
import { t } from '../../locales';

const $ = window.$ = require('jquery');

const propTypes = {
  dashboard: PropTypes.object.isRequired,
};

class Controls extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      css: props.dashboard.css || '',
      theme: props.dashboard.theme,
      refreshAble: props.dashboard.refreshAble,
      cssTemplates: [],
    };
  }
  componentWillMount() {
    $.get('/csstemplateasyncmodelview/api/read', (data) => {
      const cssTemplates = data.result.map(row => ({
        value: row.template_name,
        css: row.css,
        label: row.template_name,
      }));
      this.setState({ cssTemplates });
    });
  }
  refresh() {
    // Force refresh all slices
    this.props.dashboard.renderSlices(this.props.dashboard.sliceObjects, true);
  }
  downloadImage() {
    let dashboardTitle = this.props.dashboard.dashboard_title;
    if (dashboardTitle === null || dashboardTitle === '' || $.trim(dashboardTitle).length === 0) {
      let date = new Date();
      dashboardTitle = 1900 + date.getYear() + '-' + (1 + date.getMonth()) + '-' + date.getDate() + '-' + date.getHours() + '-' + date.getMinutes() + '-' + date.getSeconds();
    }
    html2canvas($("#grid-container"), {
      onrendered: function (canvas) {
        var imgUri = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream"); // 获取生成的图片的url  
        var save_link = document.createElementNS('http://www.w3.org/1999/xhtml', 'a');
        save_link.href = imgUri;
        save_link.download = dashboardTitle + '.png';

        var event = new MouseEvent("click", {
          bubbles: true,
          cancelable: true,
          view: window,
        });
        //var event = document.createEvent('MouseEvents');
        //event.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
        save_link.dispatchEvent(event);
      }
    });
  }
  changeCss(css) {
    this.setState({ css });
    this.props.dashboard.onChange();
  }
  changeTheme(theme) {
    this.setState({ theme });
    this.props.dashboard.onChange();
  }
  changeRefresh(refreshAble) {
    this.setState({ refreshAble });
    this.props.dashboard.onChange();
  }
  change(opt, type) {
    if (type === 'css') {
      this.changeCss(opt);
    } else if (type === 'theme') {
      this.changeTheme(opt);
    } else if (type === 'refresh') {
      this.changeRefresh(opt);
    }
  }

  getQueryString(name) {
    const reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    const r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]);
    return null;
  }

  render() {
    const dashboard = this.props.dashboard;
    const emailBody = t('Checkout this dashboard: %s', window.location.href);
    const emailLink = 'mailto:?Subject=Superset%20Dashboard%20'
      + `${dashboard.dashboard_title}&Body=${emailBody}`;
    return (
      <ButtonGroup>
        <Button
          tooltip={t('Force refresh the whole dashboard')}
          onClick={this.refresh.bind(this)}
        >
          <i className="fa fa-refresh" />
        </Button>
        <SliceAdder
          dashboard={dashboard}
          triggerNode={
            <i className="fa fa-plus" />
          }
        />
        <RefreshIntervalModal
          onChange={refreshInterval => dashboard.startPeriodicRender(refreshInterval * 1000)}
          triggerNode={
            <i className="fa fa-clock-o" />
          }
        />
        <Button
          tooltip={t('Download dashboard save as image')}
          onClick={this.downloadImage.bind(this)}
        >
          <i className="fa fa-download" />
        </Button>
        <CodeModal
          codeCallback={dashboard.readFilters.bind(dashboard)}
          triggerNode={<i className="fa fa-filter" />}
        />
        <CssEditor
          dashboard={dashboard}
          triggerNode={
            <i className="fa fa-css3" />
          }
          initialCss={dashboard.css}
          templates={this.state.cssTemplates}
          onChange={this.change.bind(this)}
          theme={dashboard.theme}
          themes={dashboard.themes}
          sliceResizeAble={dashboard.sliceResizeAble}
          refreshAble={dashboard.refreshAble}
        />
        <Button
          onClick={() => { window.location = emailLink; }}
        >
          <i className="fa fa-envelope" />
        </Button>
        <Button
          disabled={!dashboard.dash_edit_perm}
          onClick={() => {
            window.location = `/dashboardmodelview/edit/${dashboard.id}`;
          }}
          tooltip={t('Edit this dashboard\'s properties')}
        >
          <i className="fa fa-edit" />
        </Button>
        <SaveModal
          dashboard={dashboard}
          css={this.state.css}
          theme={this.state.theme}
          refreshAble={this.state.refreshAble}
          triggerNode={
            <Button disabled={!dashboard.dash_save_perm}>
              <i className="fa fa-save" />
            </Button>
          }
        />
      </ButtonGroup>
    );
  }
}
Controls.propTypes = propTypes;

export default Controls;
