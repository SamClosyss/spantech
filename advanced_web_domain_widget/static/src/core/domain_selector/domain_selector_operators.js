/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

function onDidChange(action) {
  return function (oldOperator, fieldChange) {
    if (this.category !== oldOperator.category) {
      return action(fieldChange);
    }
    return {};
  };
}

function matchValue() {
  return function ({ operator }) {
    return operator === this.value;
  };
}

const dso = registry.category("domain_selector/operator_bits");
dso.add("date_filter", {
  category: "comparison",
  label: _t("Date filter"),
  value: "date_filter",
  onDidChange: onDidChange((fieldChange) => fieldChange()),
  matches({ operator, value, fieldInfo }) {
    return operator === "date_filter";
  },
});

dso.add("=", {
  category: "equality",
  label: "=",
  value: "=",
  onDidChange: onDidChange((fieldChange) => fieldChange()),
  matches({ operator, value }) {
    return operator === this.value && typeof value !== "boolean";
  },
});
dso.add("!=", {
  category: "equality",
  label: _t("is not ="),
  value: "!=",
  onDidChange: onDidChange((fieldChange) => fieldChange()),
  matches({ operator, value }) {
    return operator === this.value && typeof value !== "boolean";
  },
});
dso.add(">", {
  category: "comparison",
  label: ">",
  value: ">",
  onDidChange: onDidChange((fieldChange) => fieldChange()),
  matches: matchValue(),
});
dso.add(">=", {
  category: "comparison",
  label: ">=",
  value: ">=",
  onDidChange: onDidChange((fieldChange) => fieldChange()),
  matches: matchValue(),
});
dso.add("<", {
  category: "comparison",
  label: "<",
  value: "<",
  onDidChange: onDidChange((fieldChange) => fieldChange()),
  matches: matchValue(),
});
dso.add("<=", {
  category: "comparison",
  label: "<=",
  value: "<=",
  onDidChange: onDidChange((fieldChange) => fieldChange()),
  matches: matchValue(),
});
dso.add("ilike", {
  category: "like",
  label: _t("contains"),
  value: "ilike",
  onDidChange: onDidChange(() => ({ value: "" })),
  matches: matchValue(),
});
dso.add("not ilike", {
  category: "like",
  label: _t("does not contain"),
  value: "not ilike",
  onDidChange: onDidChange(() => ({ value: "" })),
  matches: matchValue(),
});
dso.add("like", {
  category: "like",
  label: _t("like"),
  value: "like",
  onDidChange: onDidChange(() => ({ value: "" })),
  matches: matchValue(),
});
dso.add("not like", {
  category: "like",
  label: _t("not like"),
  value: "not like",
  onDidChange: onDidChange(() => ({ value: "" })),
  matches: matchValue(),
});
dso.add("=like", {
  category: "like",
  label: _t("=like"),
  value: "=like",
  onDidChange: onDidChange(() => ({ value: "" })),
  matches: matchValue(),
});
dso.add("=ilike", {
  category: "like",
  label: _t("=ilike"),
  value: "=ilike",
  onDidChange: onDidChange(() => ({ value: "" })),
  matches: matchValue(),
});
dso.add("child_of", {
  category: "relation",
  label: _t("child of"),
  value: "child_of",
  onDidChange: onDidChange(() => ({ value: 1 })),
  matches: matchValue(),
});
dso.add("parent_of", {
  category: "relation",
  label: _t("parent of"),
  value: "parent_of",
  onDidChange: onDidChange(() => ({ value: 1 })),
  matches: matchValue(),
});
dso.add("in", {
  category: "in",
  label: _t("in"),
  value: "in",
  onDidChange: onDidChange(() => ({ value: [] })),
  matches: matchValue(),
});
dso.add("not in", {
  category: "in",
  label: _t("not in"),
  value: "not in",
  onDidChange: onDidChange(() => ({ value: [] })),
  matches: matchValue(),
});
dso.add("set", {
  category: "set",
  label: _t("is set"),
  value: "set",
  hideValue: true,
  onDidChange() {
    return {
      operator: "!=",
      value: false,
    };
  },
  matches({ operator, value }) {
    return operator === "!=" && typeof value === "boolean";
  },
});
dso.add("not set", {
  category: "set",
  label: _t("is not set"),
  value: "not set",
  hideValue: true,
  onDidChange() {
    return {
      operator: "=",
      value: false,
    };
  },
  matches({ operator, value }) {
    return operator === "=" && typeof value === "boolean";
  },
});
