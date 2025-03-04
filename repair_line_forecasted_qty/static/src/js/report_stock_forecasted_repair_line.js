odoo.define("repair_line_forecasted_qty.RepairQtyAtDateWidget", function (require) {
  "use strict";

  var core = require("web.core");
  var QWeb = core.qweb;
  var Widget = require("web.Widget");
  var widget_registry = require("web.widget_registry");
  var utils = require("web.utils");

  var _t = core._t;

  var RepairQtyAtDateWidget = Widget.extend({
    template: "repair_line_forecasted_qty.qtyAtDate",
    events: _.extend({}, Widget.prototype.events, {
      "click .fa-area-chart": "_onClickButton",
    }),

    init: function (parent, params) {
      this.data = params.data;
      this.fields = params.fields;
      this._updateData();
      this._super(parent);
    },

    start: function () {
      var self = this;
      return this._super.apply(this, arguments).then(function () {
        self._setPopOver();
      });
    },

    _updateData: function () {
      this.data.forecasted_issue =
        this.data.available_in_location < this.data.product_uom_qty;
    },

    updateState: function (state) {
      this.$el.popover("dispose");
      var candidate = state.data[this.getParent().currentRow];
      if (candidate) {
        this.data = candidate.data;
        this._updateData();
        this.renderElement();
        this._setPopOver();
      }
    },

    async _openForecast(ev) {
      ev.stopPropagation();
      var action = await this._rpc({
        model: "product.product",
        method: "action_product_forecast_report",
        args: [[this.data.product_id.data.id]],
      });
      action.context = {
        active_model: "product.product",
        active_id: this.data.product_id.data.id,
        warehouse: this.data.warehouse_id && this.data.warehouse_id.res_id,
      };
      return this.do_action(action);
    },

    _getContent() {
      const $content = $(
        QWeb.render("repair_line_forecasted_qty.QtyDetailPopOver", {
          data: this.data,
        })
      );
      $content.on("click", ".action_open_forecast", this._openForecast.bind(this));
      return $content;
    },

    _setPopOver() {
      const $content = this._getContent();
      if (!$content) {
        return;
      }
      const options = {
        content: $content,
        html: true,
        placement: "left",
        title: _t("Availability"),
        trigger: "focus",
        delay: {show: 0, hide: 100},
      };
      this.$el.popover(options);
    },

    _onClickButton: function () {
      this.$el.find(".fa-area-chart").prop("special_click", true);
    },
  });

  widget_registry.add("repair_qty_at_date_widget", RepairQtyAtDateWidget);

  return RepairQtyAtDateWidget;
});
