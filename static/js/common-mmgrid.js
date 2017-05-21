/**
 * 为mmgrid表格中的数据添加title属性
 * @param text
 * @returns {string}
 */
function createGridHtml(text) {
    if (text == '' || text == null) {
        return '';
    } else {
        return '<span title="' + text + '">' + text + '</span>';
    }
}

var Common = {
    /**
     * 设置日期选择控件的最大日期为当前时间
     * @param selector
     * @param single
     */
    setDataRange: function (selector, single) {
        selector.daterangepicker({
            "singleDatePicker": single,
            "maxDate": new Date()
        });
    },
    setLaterDateRange: function(selector, single){
          selector.daterangepicker({
            "singleDatePicker": single,
        });
    },
    /**
     * 判断浏览器是否为IE
     * @returns {boolean}
     */
    validateIE: function () {
        var explorer = window.navigator.userAgent;
        if (explorer.indexOf("Trident") >= 0) {
            // IE 需要使用 Trident 来判断
            return true;
        }
    },
    /**
     * 验证是否为数字
     * @param value
     * @returns {boolean}
     */
    validateNumber: function(value){
        value = value.trim();
        return /^\d+$/.test(value);
    },
    /**
     * 获取当前日期
     * @returns {string}
     */
    getNow: function () {
        var now = new Date();
        var yy = now.getFullYear();
        var mm = now.getMonth() + 1;
        var dd = now.getDate();
        return yy + "-" + mm + "-" + dd;
    },
    /**
     * 验证日期选择控件中的日期区间是否符合规则
     * @param rd
     * @returns {boolean}
     */
    validateRangeDate: function (rd) {
        rd = $.trim(rd);
        return /^\d{4}-\d{2}-\d{2}\s*~\s*\d{4}-\d{2}-\d{2}$/.test(rd);
    },
    /**
     * 判断是否为空值
     * @param data
     * @returns {boolean}
     */
    isNull: function (data) {
        if (data.indexOf("请") > -1) {
            return true
        }
        return /^\s*$/gi.test(data)
    },
    /**
     * 拼接参数
     * @param args
     */
    contactParams: function (args) {
        var obj = {};
        for (var key in args) {
            var val = args[key].val();
            if (!this.isNull(val)) {
                obj[key] = val;
            }
        }
        return obj;
    },
    /**
     * 渲染mmgrid
     * @param table
     * @param cols
     * @param url
     * @param method
     * @param plugins
     * @param paramsFunc
     */
    renderGrid: function (table, cols, url, method, plugins, paramsFunc) {
        return table.mmGrid({
            cols: cols,
            height: "auto",
            url: url,
            method: method,
            remoteSort: true,
            fullWidthRows: true,
            sortName: 'SECUCODE',
            sortStatus: 'asc',
            nowrap: true,
            plugins: [plugins.mmPaginator()],
            params: function () {
                return paramsFunc();
            }
        });
    },
    /**
     * mmgrid绑定过滤事件
     * @param selector
     * @param mmg
     */
    filterGrid: function(selector, mmg){
        selector.bind("click", function () {
            // 筛选后重新加载表格数据
            mmg.load({page: 1});
        });
    }
};

var Convert = {
    /**
     * 字符串转换成日期
     * @param value
     * @returns {Date}
     */
    str2date: function (value) {
        return new Date(value);
    }
};