function __export(m) {
    for (var p in m) if (!exports.hasOwnProperty(p)) exports[p] = m[p];
}
Object.defineProperty(exports, "__esModule", { value: true });
__export(require("./ui-listview.common"));
var observableArray = require("tns-core-modules/data/observable-array");
var listViewCommonModule = require("./ui-listview.common");
var layoutsModule = require("tns-core-modules/ui/layouts/stack-layout");
var applicationModule = require("tns-core-modules/application");
var view_1 = require("tns-core-modules/ui/core/view");
var color_1 = require("tns-core-modules/color");
var utilsModule = require("tns-core-modules/utils/utils");
var lastFiredEvent;
var lastSelectedIndex;
var knownTemplates;
(function (knownTemplates) {
    knownTemplates.itemTemplate = "itemTemplate";
    knownTemplates.itemSwipeTemplate = "itemSwipeTemplate";
    knownTemplates.loadOnDemandItemTemplate = "loadOnDemandItemTemplate";
    knownTemplates.headerItemTemplate = "headerItemTemplate";
    knownTemplates.footerItemTemplate = "footerItemTemplate";
    knownTemplates.groupTemplate = "groupTemplate";
})(knownTemplates = exports.knownTemplates || (exports.knownTemplates = {}));
var knownMultiTemplates;
(function (knownMultiTemplates) {
    knownMultiTemplates.itemTemplates = "itemTemplates";
})(knownMultiTemplates = exports.knownMultiTemplates || (exports.knownMultiTemplates = {}));
var ReorderHandle = /** @class */ (function (_super) {
    __extends(ReorderHandle, _super);
    function ReorderHandle() {
        return _super.call(this) || this;
    }
    return ReorderHandle;
}(listViewCommonModule.ReorderHandle));
exports.ReorderHandle = ReorderHandle;
function patchHolderViewIfChanged(holder, view) {
    if (view !== holder['nsView']._subViews[0]) {
        // the view has been changed on the event handler
        holder['nsView'].removeChildren();
        holder['nsView'].addChild(view);
    }
}
var ExtendedReorderWithHandlesBehaviorClass;
function ensureExtendedReorderWithHandlesBehavior() {
    if (ExtendedReorderWithHandlesBehaviorClass) {
        return;
    }
    var ExtendedReorderWithHandlesBehavior = /** @class */ (function (_super) {
        __extends(ExtendedReorderWithHandlesBehavior, _super);
        function ExtendedReorderWithHandlesBehavior(viewId) {
            var _this = _super.call(this, viewId) || this;
            return global.__native(_this);
        }
        ExtendedReorderWithHandlesBehavior.prototype.getReorderHandleOverride = function (itemView) {
            var originalItemIndex = this.owner().getChildAdapterPosition(itemView);
            var nsViewForItem = this.nsOwner._listViewAdapter.getViewForItem(this.nsOwner.getItemAtIndex(originalItemIndex));
            var reorderHandle = undefined;
            nsViewForItem.eachChildView(function (view) {
                if (view instanceof ReorderHandle) {
                    reorderHandle = view;
                    return false;
                }
                return true;
            });
            return reorderHandle === undefined ? itemView : reorderHandle.nativeViewProtected;
        };
        return ExtendedReorderWithHandlesBehavior;
    }(com.telerik.widget.list.ReorderWithHandlesBehavior));
    ExtendedReorderWithHandlesBehaviorClass = ExtendedReorderWithHandlesBehavior;
}
var ListViewAdapterClass;
function ensureListViewAdapter() {
    if (ListViewAdapterClass) {
        return;
    }
    // We need this class because it is the point where we plug-in into the listView
    // and use the defined itemTemplate to create the native Android item views and
    // pass it to the control.
    var ListViewAdapter = /** @class */ (function (_super) {
        __extends(ListViewAdapter, _super);
        function ListViewAdapter(items, listView) {
            var _this = _super.call(this, items) || this;
            _this._selectionViewId = applicationModule.android.context.getResources().getIdentifier("selectable_item_background", "drawable", applicationModule.android.context.getPackageName());
            _this.templateTypeNumberString = new Map();
            _this._currentNativeItemType = 0;
            _this.ownerLv = new WeakRef(listView);
            _this._viewHolders = new Array();
            _this._swipeHolders = new Array();
            _this._viewHolderChildren = new Array();
            return global.__native(_this);
        }
        ListViewAdapter.prototype.disposeViewHolderViews = function () {
            this._viewHolders = null;
            this._swipeHolders = null;
            var owner = this.ownerLv.get();
            this._viewHolderChildren.forEach(function (element) {
                if (!(element.parent instanceof RadListView)) {
                    owner._removeView(element.parent);
                }
                element.parent._removeView(element);
            });
        };
        ListViewAdapter.prototype.getKeyByValue = function (inputValue) {
            var result;
            this.templateTypeNumberString.forEach(function (value, key, map) {
                if (value === inputValue) {
                    result = key;
                }
            }, this);
            return result;
        };
        ListViewAdapter.prototype.clearTemplateTypes = function () {
            this._currentNativeItemType = 0;
            this.templateTypeNumberString.clear();
        };
        ListViewAdapter.prototype.onCreateViewHolder = function (parent, viewType) {
            var templateType = this.getKeyByValue(viewType);
            var owner = this.ownerLv.get();
            var view = owner.getViewForViewType(listViewCommonModule.ListViewViewTypes.ItemView, templateType);
            var parentView = new layoutsModule.StackLayout();
            var layoutParams = owner._getViewLayoutParams();
            parentView.orientation = "vertical";
            parentView.addChild(view);
            this._viewHolderChildren.push(parentView);
            owner._addView(parentView);
            parentView.nativeView.setLayoutParams(layoutParams);
            parentView.nativeView.setBackgroundResource(this._selectionViewId);
            var holder = new com.telerik.widget.list.ListViewHolder(parentView.nativeView);
            holder['nsView'] = parentView;
            this._viewHolders.push(holder);
            return holder;
        };
        ListViewAdapter.prototype.getItemViewType = function (position) {
            var resultType = 0;
            var owner = this.ownerLv.get();
            if (owner.itemTemplateSelector) {
                var selector = owner.itemTemplateSelector;
                if (selector) {
                    var selectorType = selector(owner.getItemAtIndex(position), position, owner.items);
                    if (!this.templateTypeNumberString.has(selectorType)) {
                        this.templateTypeNumberString.set(selectorType, this._currentNativeItemType);
                        this._currentNativeItemType++;
                    }
                    resultType = this.templateTypeNumberString.get(selectorType);
                }
            }
            return resultType;
        };
        ListViewAdapter.prototype.onBindViewHolder = function (holder, position) {
            var owner = this.ownerLv.get();
            holder['nsView'].bindingContext = owner.getItemAtIndex(position);
            var internalLoadingArgs = {
                eventName: listViewCommonModule.RadListView.itemLoadingInternalEvent,
                index: position,
                object: owner,
                view: holder['nsView']._subViews[0],
                android: holder
            };
            owner.notify(internalLoadingArgs);
            var args = {
                eventName: listViewCommonModule.RadListView.itemLoadingEvent,
                index: position,
                object: owner,
                view: holder['nsView']._subViews[0],
                android: holder
            };
            owner.notify(args);
            patchHolderViewIfChanged(holder, args.view);
        };
        ListViewAdapter.prototype.onCreateSwipeContentHolder = function (parent) {
            var owner = this.ownerLv.get();
            var swipeView = owner.getViewForViewType(listViewCommonModule.ListViewViewTypes.ItemSwipeView);
            this._viewHolderChildren.push(swipeView);
            owner._addView(swipeView);
            var holder = new com.telerik.widget.list.ListViewHolder(swipeView.nativeView);
            holder['nsView'] = swipeView;
            this._swipeHolders.push(holder);
            return holder;
        };
        ListViewAdapter.prototype.onBindSwipeContentHolder = function (holder, position) {
            holder['nsView'].bindingContext = this.ownerLv.get().getItemAtIndex(position);
        };
        ListViewAdapter.prototype.canReorder = function (itemIndex) {
            var owner = this.ownerLv.get();
            var result = _super.prototype.canReorder.call(this, itemIndex);
            var view = owner.getViewForItem(owner.getItemAtIndex(itemIndex));
            var args = {
                eventName: listViewCommonModule.RadListView.itemReorderStartingEvent,
                object: owner,
                index: itemIndex,
                groupIndex: -1,
                data: undefined,
                returnValue: true,
                view: view
            };
            owner.notify(args);
            return args.returnValue;
        };
        ListViewAdapter.prototype.reorderItem = function (oldPosition, newPosition) {
            var result = _super.prototype.reorderItem.call(this, oldPosition, newPosition);
            if (result === true) {
                this.ownerLv.get()._reorderItemInSource(oldPosition, newPosition);
            }
            return result;
        };
        ListViewAdapter.prototype.setItems = function (items) {
            this._viewHolders.splice(0, this._viewHolders.length);
            this._swipeHolders.splice(0, this._swipeHolders.length);
            this.ownerLv.get()._resetCurrentId();
            _super.prototype.setItems.call(this, items);
        };
        ListViewAdapter.prototype.canSwipe = function (position) {
            if (!_super.prototype.canSwipe.call(this, position)) {
                return false;
            }
            var owner = this.ownerLv.get();
            var args = {
                eventName: listViewCommonModule.RadListView.itemSwipingEvent,
                object: owner,
                index: position,
                groupIndex: -1,
                returnValue: true
            };
            owner.notify(args);
            return args.returnValue;
        };
        ListViewAdapter.prototype.canSelect = function (position) {
            var canSelect = true;
            var owner = this.ownerLv.get();
            if (owner.items) {
                var dataItem = owner.getItemAtIndex(position);
                var isSelected = owner.isItemSelected(dataItem);
                var currentEventName = isSelected === true ? listViewCommonModule.RadListView.itemDeselectingEvent : listViewCommonModule.RadListView.itemSelectingEvent;
                var view = owner.getViewForItem(dataItem);
                var args = {
                    eventName: currentEventName,
                    object: owner,
                    index: position,
                    groupIndex: -1,
                    returnValue: true,
                    view: view
                };
                if ((lastSelectedIndex !== position) || (lastSelectedIndex === position && lastFiredEvent !== currentEventName)) {
                    lastSelectedIndex = position;
                    owner.notify(args);
                    canSelect = args.returnValue === true;
                    lastFiredEvent = currentEventName;
                }
            }
            return canSelect;
        };
        ListViewAdapter.prototype.getViewForItem = function (item) {
            for (var i = 0; i < this._viewHolders.length; i++) {
                if (this._viewHolders[i]['nsView'] && this._viewHolders[i]['nsView'].bindingContext === item) {
                    return this._viewHolders[i]['nsView'].getChildAt(0);
                }
            }
            return undefined;
        };
        ListViewAdapter.prototype.getSwipeViewForItem = function (item) {
            for (var i = 0; i < this._swipeHolders.length; i++) {
                if (this._swipeHolders[i]['nsView'] && this._swipeHolders[i]['nsView'].bindingContext === item) {
                    return this._swipeHolders[i]['nsView'];
                }
            }
            return undefined;
        };
        return ListViewAdapter;
    }(com.telerik.widget.list.ListViewAdapter));
    ListViewAdapterClass = ListViewAdapter;
}
var ListViewDataSourceAdapterClass;
function ensureListViewDataSourceAdapter() {
    if (ListViewDataSourceAdapterClass) {
        return;
    }
    var ListViewDataSourceAdapter = /** @class */ (function (_super) {
        __extends(ListViewDataSourceAdapter, _super);
        function ListViewDataSourceAdapter(items, listView) {
            var _this = _super.call(this, items) || this;
            _this.templateTypeNumberString = new Map();
            _this._currentNativeItemType = 0;
            _this._selectionViewId = applicationModule.android.context.getResources().getIdentifier("selectable_item_background", "drawable", applicationModule.android.context.getPackageName());
            _this.ownerLv = new WeakRef(listView);
            _this._viewHolders = new Array();
            _this._swipeHolders = new Array();
            _this._viewHolderChildren = new Array();
            return global.__native(_this);
        }
        ListViewDataSourceAdapter.prototype.disposeViewHolderViews = function () {
            this._viewHolders = null;
            this._swipeHolders = null;
            var owner = this.ownerLv.get();
            this._viewHolderChildren.forEach(function (element) {
                if (!(element.parent instanceof RadListView)) {
                    owner._removeView(element.parent);
                }
                element.parent._removeView(element);
            });
        };
        ListViewDataSourceAdapter.prototype.getKeyByValue = function (inputValue) {
            var result;
            this.templateTypeNumberString.forEach(function (value, key, map) {
                if (value === inputValue) {
                    result = key;
                }
            }, this);
            return result;
        };
        ListViewDataSourceAdapter.prototype.clearTemplateTypes = function () {
            this._currentNativeItemType = 0;
            this.templateTypeNumberString.clear();
        };
        ListViewDataSourceAdapter.prototype.onCreateGroupViewHolder = function (parent, viewType) {
            var owner = this.ownerLv.get();
            if (owner.enableCollapsibleGroups) {
                return _super.prototype.onCreateGroupViewHolder.call(this, parent, viewType);
            }
            var nsGroupView = owner.getViewForViewType(listViewCommonModule.ListViewViewTypes.GroupView);
            if (!nsGroupView) {
                return _super.prototype.onCreateGroupViewHolder.call(this, parent, viewType);
            }
            var layoutParams = owner._getViewLayoutParams();
            if (nsGroupView) {
                this._viewHolderChildren.push(nsGroupView);
                owner._addView(nsGroupView);
                nsGroupView.nativeView.setLayoutParams(layoutParams);
            }
            var holder = new com.telerik.widget.list.ListViewHolder(nsGroupView.android);
            holder['nsView'] = nsGroupView;
            this._viewHolders.push(holder);
            return holder;
        };
        ListViewDataSourceAdapter.prototype.onBindGroupViewHolder = function (holder, groupKey) {
            var owner = this.ownerLv.get();
            if (owner.enableCollapsibleGroups || !holder['nsView']) {
                _super.prototype.onBindGroupViewHolder.call(this, holder, groupKey);
            }
            else {
                var value = { category: groupKey };
                holder['nsView'].bindingContext = value;
                var internalLoadingArgs = {
                    eventName: listViewCommonModule.RadListView.itemLoadingInternalEvent,
                    index: -1,
                    object: owner,
                    view: holder['nsView'],
                    android: holder
                };
                owner.notify(internalLoadingArgs);
                var args = {
                    eventName: listViewCommonModule.RadListView.itemLoadingEvent,
                    index: -1,
                    object: owner,
                    view: holder['nsView'],
                    android: holder
                };
                owner.notify(args);
            }
        };
        ListViewDataSourceAdapter.prototype.onCreateItemViewHolder = function (parent, viewType) {
            var owner = this.ownerLv.get();
            var templateType = this.getKeyByValue(viewType);
            var view = owner.getViewForViewType(listViewCommonModule.ListViewViewTypes.ItemView, templateType);
            var parentView = new layoutsModule.StackLayout();
            var layoutParams = owner._getViewLayoutParams();
            parentView.orientation = "vertical";
            parentView.addChild(view);
            this._viewHolderChildren.push(parentView);
            owner._addView(parentView);
            parentView.android.setLayoutParams(layoutParams);
            parentView.android.setBackgroundResource(this._selectionViewId);
            var holder = new com.telerik.widget.list.ListViewHolder(parentView.android);
            holder['nsView'] = parentView;
            this._viewHolders.push(holder);
            return holder;
        };
        ListViewDataSourceAdapter.prototype.isGroupHeader = function (position) {
            return _super.prototype.isGroupHeader.call(this, position);
        };
        ListViewDataSourceAdapter.prototype.getItemViewType = function (position) {
            var owner = this.ownerLv.get();
            var resultType = 0;
            if (_super.prototype.isGroupHeader.call(this, position)) {
                resultType = _super.prototype.getItemViewType.call(this, position);
            }
            else {
                if (owner.itemTemplateSelector) {
                    var selector = owner.itemTemplateSelector;
                    if (selector) {
                        var nativeIndex = _super.prototype.getItemId.call(this, position);
                        var dataItem = owner.getItemAtIndex(nativeIndex);
                        if (dataItem) {
                            var selectorType = selector(dataItem, nativeIndex, owner.items);
                            if (!this.templateTypeNumberString.has(selectorType)) {
                                this.templateTypeNumberString.set(selectorType, this._currentNativeItemType);
                                this._currentNativeItemType++;
                            }
                            resultType = this.templateTypeNumberString.get(selectorType);
                        }
                    }
                }
            }
            return resultType;
        };
        ListViewDataSourceAdapter.prototype.onBindItemViewHolder = function (holder, position) {
            var owner = this.ownerLv.get();
            holder['nsView'].bindingContext = owner.getItemAtIndex(position);
            var internalLoadingArgs = {
                eventName: listViewCommonModule.RadListView.itemLoadingInternalEvent,
                index: position,
                object: owner,
                view: holder['nsView']._subViews[0],
                android: holder
            };
            owner.notify(internalLoadingArgs);
            var args = {
                eventName: listViewCommonModule.RadListView.itemLoadingEvent,
                index: position,
                object: owner,
                view: holder['nsView']._subViews[0],
                android: holder
            };
            owner.notify(args);
            patchHolderViewIfChanged(holder, args.view);
        };
        ListViewDataSourceAdapter.prototype.onCreateSwipeContentHolder = function (parent) {
            var owner = this.ownerLv.get();
            var swipeView = owner.getViewForViewType(listViewCommonModule.ListViewViewTypes.ItemSwipeView);
            this._viewHolderChildren.push(swipeView);
            owner._addView(swipeView);
            var holder = new com.telerik.widget.list.ListViewHolder(swipeView.android);
            holder['nsView'] = swipeView;
            this._swipeHolders.push(holder);
            return holder;
        };
        ListViewDataSourceAdapter.prototype.onBindSwipeContentHolder = function (holder, position) {
            var owner = this.ownerLv.get();
            holder['nsView'].bindingContext = owner.getItemAtIndex(owner._getOriginalIndex(position));
        };
        ListViewDataSourceAdapter.prototype.reorderItem = function (oldPosition, newPosition) {
            var result = _super.prototype.reorderItem.call(this, oldPosition, newPosition);
            if (result === true) {
                this.ownerLv.get()._reorderItemInSource(oldPosition, newPosition);
            }
            return result;
        };
        ListViewDataSourceAdapter.prototype.setItems = function (items) {
            this._viewHolders.splice(0, this._viewHolders.length);
            this._swipeHolders.splice(0, this._swipeHolders.length);
            this.ownerLv.get()._resetCurrentId();
            _super.prototype.setItems.call(this, items);
        };
        ListViewDataSourceAdapter.prototype.canSwipe = function (position) {
            var owner = this.ownerLv.get();
            if (!_super.prototype.canSwipe.call(this, position)) {
                return false;
            }
            var args = {
                eventName: listViewCommonModule.RadListView.itemSwipingEvent,
                object: owner,
                index: position,
                groupIndex: -1,
                returnValue: true
            };
            owner.notify(args);
            return args.returnValue;
        };
        ListViewDataSourceAdapter.prototype.canSelect = function (position) {
            var owner = this.ownerLv.get();
            if (owner.items) {
                var isSelected = owner.isItemSelected(owner.getItemAtIndex(position));
                var currentEventName = isSelected === true ? listViewCommonModule.RadListView.itemDeselectingEvent : listViewCommonModule.RadListView.itemSelectingEvent;
                var args = {
                    eventName: currentEventName,
                    object: owner,
                    index: position,
                    groupIndex: -1,
                    returnValue: true
                };
                if ((lastSelectedIndex !== position) || (lastSelectedIndex === position && lastFiredEvent !== currentEventName)) {
                    lastSelectedIndex = position;
                    owner.notify(args);
                    lastFiredEvent = currentEventName;
                }
            }
            return true;
        };
        ListViewDataSourceAdapter.prototype.getViewForItem = function (item) {
            for (var i = 0; i < this._viewHolders.length; i++) {
                if (this._viewHolders[i]['nsView'] && this._viewHolders[i]['nsView'].bindingContext === item) {
                    return this._viewHolders[i]['nsView'].getChildAt(0);
                }
            }
            return undefined;
        };
        ListViewDataSourceAdapter.prototype.getSwipeViewForItem = function (item) {
            for (var i = 0; i < this._swipeHolders.length; i++) {
                if (this._swipeHolders[i]['nsView'] && this._swipeHolders[i]['nsView'].bindingContext === item) {
                    return this._swipeHolders[i]['nsView'];
                }
            }
            return undefined;
        };
        return ListViewDataSourceAdapter;
    }(com.telerik.widget.list.ListViewDataSourceAdapter));
    ListViewDataSourceAdapterClass = ListViewDataSourceAdapter;
}
var RadListView = /** @class */ (function (_super) {
    __extends(RadListView, _super);
    function RadListView() {
        var _this = _super.call(this) || this;
        _this._currentId = 0;
        _this._androidViewId = -1;
        ensureListViewAdapter();
        ensureListViewDataSourceAdapter();
        _this.listViewLayout = new ListViewLinearLayout();
        _this.on("bindingContextChange", _this.bindingContextChanged, _this);
        _this._headerViewHolderChildren = new Array();
        _this._footerViewHolderChildren = new Array();
        _this._loadOnDemandViewHolderChildren = new Array();
        return _this;
    }
    RadListView.prototype.createNativeView = function () {
        this._android = new com.telerik.widget.list.RadListView(this._context);
        this._rootLayout = new android.widget.FrameLayout(this._context);
        this._rootLayout.addView(this._android);
        if (this.listViewLayout) {
            this.listViewLayout._onOwnerUICreated();
        }
        else {
            this.listViewLayout = new ListViewLinearLayout();
        }
        this.loadData();
        this.subscribeForNativeScrollEvents();
        this.updateSelectionBehavior();
        this.updateReorderBehavior();
        this.updateLoadOnDemandBehavior();
        this.updatePullToRefreshBehavior();
        this.updateSwipeToExecuteBehavior();
        this.updateSwipeActionsBehavior();
        this.updateCollapsibleGroupsBehavior();
        this._updateHeader();
        this._updateFooter();
        var that = new WeakRef(this);
        this._android.addItemClickListener(new com.telerik.widget.list.RadListView.ItemClickListener({
            onItemClick: function (itemPosition, motionEvent) {
                var listView = that.get();
                var isGroupHeader = listView._listViewAdapter.isGroupHeader(itemPosition);
                if (!isGroupHeader) {
                    var originalPosition = listView._getOriginalIndex(itemPosition);
                    var tappedView = listView._listViewAdapter.getViewForItem(listView.getItemAtIndex(originalPosition));
                    var args = {
                        android: motionEvent,
                        eventName: listViewCommonModule.RadListView.itemTapEvent,
                        object: listView,
                        view: tappedView,
                        index: originalPosition,
                        groupIndex: -1
                    };
                    that.get().notify(args);
                }
            },
            onItemLongClick: function (itemPosition, motionEvent) {
                var listView = that.get();
                var isGroupHeader = listView._listViewAdapter.isGroupHeader(itemPosition);
                if (!isGroupHeader) {
                    var originalPosition = listView._getOriginalIndex(itemPosition);
                    var tappedView = listView._listViewAdapter.getViewForItem(listView.getItemAtIndex(originalPosition));
                    var args = {
                        android: motionEvent,
                        eventName: listViewCommonModule.RadListView.itemHoldEvent,
                        object: listView,
                        view: tappedView,
                        index: originalPosition,
                        groupIndex: -1
                    };
                    that.get().notify(args);
                }
            }
        }));
        return this._rootLayout;
    };
    RadListView.prototype.initNativeView = function () {
        _super.prototype.initNativeView.call(this);
        if (this._androidViewId < 0) {
            this._androidViewId = android.view.View.generateViewId();
        }
        this._android.setId(this._androidViewId);
    };
    RadListView.prototype.disposeNativeView = function () {
        if (this._scrollStateListener) {
            this._android.removeOnScrollListener(this._scrollStateListener);
        }
        if (this._selectionBehavior) {
            this._android.removeBehavior(this._selectionBehavior);
            this._selectionBehavior = undefined;
        }
        if (this._reorderBehavior) {
            this._android.removeBehavior(this._reorderBehavior);
            this._reorderBehavior = undefined;
        }
        if (this._loadOnDemandBehavior) {
            this._android.removeBehavior(this._loadOnDemandBehavior);
            this._loadOnDemandBehavior = undefined;
        }
        if (this._swipeExecuteBehavior) {
            this._android.removeBehavior(this._swipeExecuteBehavior);
            this._swipeExecuteBehavior = undefined;
        }
        if (this._swipeActionsBehavior) {
            this._android.removeBehavior(this._swipeActionsBehavior);
            this._swipeActionsBehavior = undefined;
        }
        if (this._pullToRefreshBehavior) {
            this._android.removeBehavior(this._pullToRefreshBehavior);
            this._pullToRefreshBehavior = undefined;
        }
        if (this._android) {
            this._android.setAdapter(null);
        }
        _super.prototype.disposeNativeView.call(this);
    };
    RadListView.prototype._resetCurrentId = function () {
        this._currentId = 0;
    };
    RadListView.prototype._getUniqueItemId = function () {
        return this._currentId++;
    };
    Object.defineProperty(RadListView.prototype, "androidListView", {
        get: function () {
            return this._android;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(RadListView.prototype, "_childrenCount", {
        get: function () {
            var templatesCount = 0;
            if (this._headerView) {
                templatesCount++;
            }
            if (this._footerView) {
                templatesCount++;
            }
            if (this._listViewAdapter === undefined) {
                return 0;
            }
            if (!this._listViewAdapter._viewHolders) {
                return 0;
            }
            return this._listViewAdapter._viewHolders.length + this._listViewAdapter._swipeHolders.length + templatesCount;
        },
        enumerable: true,
        configurable: true
    });
    RadListView.prototype.eachChildView = function (callback) {
        if (this._headerView) {
            callback(this._headerView);
        }
        if (this._footerView) {
            callback(this._footerView);
        }
        if (this._listViewAdapter === undefined) {
            return;
        }
        if (this._listViewAdapter._viewHolders) {
            this._listViewAdapter._viewHolders.forEach(function (value, key) {
                callback(value['nsView']);
            }, this);
        }
        if (this._listViewAdapter._swipeHolders) {
            this._listViewAdapter._swipeHolders.forEach(function (value, key) {
                callback(value['nsView']);
            }, this);
        }
    };
    RadListView.prototype._getViewLayoutParams = function () {
        var layoutParams = new org.nativescript.widgets.CommonLayoutParams();
        if (this.listViewLayout instanceof ListViewLinearLayout) {
            if (this.listViewLayout.scrollDirection.toLowerCase() === listViewCommonModule.ListViewScrollDirection.Vertical.toLowerCase()) {
                layoutParams.width = org.nativescript.widgets.CommonLayoutParams.MATCH_PARENT;
                layoutParams.height = org.nativescript.widgets.CommonLayoutParams.WRAP_CONTENT;
            }
            else if (this.listViewLayout.scrollDirection.toLowerCase() === listViewCommonModule.ListViewScrollDirection.Horizontal.toLowerCase()) {
                layoutParams.width = org.nativescript.widgets.CommonLayoutParams.WRAP_CONTENT;
                layoutParams.height = org.nativescript.widgets.CommonLayoutParams.MATCH_PARENT;
            }
        }
        return layoutParams;
    };
    RadListView.prototype.isItemSelected = function (item) {
        if (this._selectionBehavior) {
            var nativeSelectedItems = this._selectionBehavior.selectedItems();
            for (var i = 0; i < nativeSelectedItems.size(); i++) {
                var nativeSelectedItem = nativeSelectedItems.get(i);
                var currentNativeIndex = this._listViewAdapter.getItems().indexOf(nativeSelectedItem);
                var sourceSelectedItem = this.getItemAtIndex(currentNativeIndex);
                if (sourceSelectedItem === item) {
                    return true;
                }
            }
        }
        return false;
    };
    RadListView.prototype.selectAll = function () {
        _super.prototype.selectAll.call(this);
        if (!this.items) {
            return;
        }
        if (this._selectionBehavior) {
            for (var i = 0; i < this.items.length; i++) {
                this._selectionBehavior.changeIsSelected(i, true);
            }
        }
    };
    RadListView.prototype.deselectAll = function () {
        if (!this.items) {
            return;
        }
        if (this._selectionBehavior) {
            for (var i = 0; i < this.items.length; i++) {
                this._selectionBehavior.changeIsSelected(i, false);
            }
        }
    };
    RadListView.prototype.selectItemAt = function (index) {
        if (this._selectionBehavior) {
            this._selectionBehavior.changeIsSelected(index, true);
        }
    };
    RadListView.prototype.deselectItemAt = function (index) {
        if (this._selectionBehavior) {
            this._selectionBehavior.changeIsSelected(index, false);
        }
    };
    RadListView.prototype.getViewForItem = function (item) {
        if (item === undefined) {
            throw new Error("Item must be an object from the currently assigned source.");
        }
        if (this._listViewAdapter === undefined) {
            return undefined;
        }
        return this._listViewAdapter.getViewForItem(item);
    };
    RadListView.prototype.getSelectedItems = function () {
        if (this._selectionBehavior) {
            var selectedItems = new Array();
            var nativeSelectedItems = this._selectionBehavior.selectedItems();
            for (var i = 0; i < nativeSelectedItems.size(); i++) {
                selectedItems.push(this.getItemAtIndex(this._android.getAdapter().getItems().indexOf(nativeSelectedItems.get(i))));
            }
            return selectedItems;
        }
        return _super.prototype.getSelectedItems.call(this);
    };
    RadListView.prototype._getGroupTemplateBindingContext = function () {
        return null;
    };
    RadListView.prototype.onPullToRefreshStyleChanged = function (oldValue, newValue) {
        this.updatePullToRefreshBehavior();
    };
    RadListView.prototype.onItemViewLoaderChanged = function () {
        if (this.itemViewLoader) {
            this.updateSelectionBehavior();
            this.updateReorderBehavior();
            this.updateLoadOnDemandBehavior();
            this.updatePullToRefreshBehavior();
            this.updateSwipeToExecuteBehavior();
            this.loadData();
        }
    };
    RadListView.prototype.onHeaderItemTemplateChanged = function (oldValue, newValue) {
        _super.prototype.onHeaderItemTemplateChanged.call(this, oldValue, newValue);
        if (this._android) {
            this._updateHeader();
        }
    };
    RadListView.prototype.onFooterItemTemplateChanged = function (oldValue, newValue) {
        _super.prototype.onFooterItemTemplateChanged.call(this, oldValue, newValue);
        if (this._android) {
            this._updateFooter();
        }
    };
    RadListView.prototype.onListViewLayoutChanged = function (oldValue, newValue) {
        _super.prototype.onListViewLayoutChanged.call(this, oldValue, newValue);
        if (oldValue) {
            var newLayout = oldValue;
            newLayout._reset();
        }
        if (newValue) {
            var newLayout = newValue;
            newLayout._init(this);
        }
    };
    RadListView.prototype.onItemTemplateSelectorChanged = function (oldValue, newValue) {
        _super.prototype.onItemTemplateSelectorChanged.call(this, oldValue, newValue);
        if (this._listViewAdapter) {
            this._listViewAdapter.clearTemplateTypes();
        }
        this.loadData();
    };
    RadListView.prototype.onItemTemplateChanged = function (oldValue, newValue) {
        _super.prototype.onItemTemplateChanged.call(this, oldValue, newValue); // TODO: update current template with the new one
        this.loadData();
    };
    RadListView.prototype.onGroupTemplateChanged = function (oldValue, newValue) {
        _super.prototype.onGroupTemplateChanged.call(this, oldValue, newValue);
        if (this._android) {
            this._updateHeader();
            this._updateFooter();
        }
    };
    RadListView.prototype.onItemTemplatesChanged = function (oldValue, newValue) {
        _super.prototype.onItemTemplatesChanged.call(this, oldValue, newValue);
        this.loadData();
    };
    RadListView.prototype.itemSwipeTemplateChanged = function (oldValue, newValue) {
        _super.prototype.onItemSwipeTemplateChanged.call(this, oldValue, newValue);
        this.updateSwipeToExecuteBehavior();
        this.updateSwipeActionsBehavior();
        this.loadData();
    };
    RadListView.prototype.onMultipleSelectionChanged = function (oldValue, newValue) {
        _super.prototype.onMultipleSelectionChanged.call(this, oldValue, newValue);
        this.updateSelectionBehavior();
    };
    RadListView.prototype.onItemReorderChanged = function (oldValue, newValue) {
        _super.prototype.onItemReorderChanged.call(this, oldValue, newValue);
        this.updateReorderBehavior();
    };
    RadListView.prototype.onItemSwipeChanged = function (oldValue, newValue) {
        _super.prototype.onItemSwipeChanged.call(this, oldValue, newValue);
        this.updateSwipeToExecuteBehavior();
    };
    RadListView.prototype.onSwipeActionsChanged = function (oldValue, newValue) {
        _super.prototype.onSwipeActionsChanged.call(this, oldValue, newValue);
        this.updateSwipeActionsBehavior();
    };
    RadListView.prototype.onPullToRefreshChanged = function (oldValue, newValue) {
        _super.prototype.onPullToRefreshChanged.call(this, oldValue, newValue);
        this.updatePullToRefreshBehavior();
    };
    RadListView.prototype.onLoadOnDemandModeChanged = function (oldValue, newValue) {
        _super.prototype.onLoadOnDemandModeChanged.call(this, oldValue, newValue);
        this.setLoadOnDemandModeInternal(newValue);
    };
    RadListView.prototype.onLoadOnDemandBufferSizeChanged = function (oldValue, newValue) {
        _super.prototype.onLoadOnDemandBufferSizeChanged.call(this, oldValue, newValue);
        this.updateLoadOnDemandBehavior();
    };
    RadListView.prototype.onSelectionBehaviorChanged = function (oldValue, newValue) {
        _super.prototype.onSelectionBehaviorChanged.call(this, oldValue, newValue);
        this.updateSelectionBehavior();
    };
    RadListView.prototype.onLoadOnDemandItemTemplateChanged = function (oldValue, newValue) {
        _super.prototype.onLoadOnDemandItemTemplateChanged.call(this, oldValue, newValue);
        this.updateLoadOnDemandBehavior();
    };
    RadListView.prototype.onSourceCollectionChanged = function (data) {
        if (this._android === undefined) {
            return;
        }
        if (data.action === observableArray.ChangeType.Update) {
            var itemValue = this._listViewAdapter.getItem(data.index);
            this._listViewAdapter.remove(data.index);
            this._listViewAdapter.add(data.index, itemValue);
        }
        else if (data.action === observableArray.ChangeType.Delete) {
            this._listViewAdapter.remove(data.index);
        }
        else if (data.action === observableArray.ChangeType.Add) {
            for (var i = 0; i < data.addedCount; i++) {
                if (isNaN(data.index)) {
                    this._listViewAdapter.add(new java.lang.Integer(this._getUniqueItemId()));
                }
                else {
                    this._listViewAdapter.add(data.index, new java.lang.Integer(this._getUniqueItemId()));
                }
            }
        }
        else if (data.action === observableArray.ChangeType.Splice) {
            if (data.removed && (data.removed.length > 0)) {
                for (var i = 0; i < data.removed.length; i++) {
                    this._listViewAdapter.remove(data.index + (data.removed.length - 1) - i);
                }
            }
            else {
                for (var i = 0; i < data.addedCount; i++) {
                    this._listViewAdapter.add(data.index + i, new java.lang.Integer(this._getUniqueItemId()));
                }
            }
        }
    };
    RadListView.prototype.onEnableCollapsibleGroupsChanged = function (oldValue, newValue) {
        this.loadData();
    };
    RadListView.prototype.onGroupingFunctionChanged = function (oldValue, newValue) {
        _super.prototype.onGroupingFunctionChanged.call(this, oldValue, newValue);
        if (newValue) {
            this.loadData();
        }
        else {
            this.clearGroupDescriptors();
        }
    };
    RadListView.prototype.onFilteringFunctionChanged = function (oldValue, newValue) {
        if (newValue) {
            this.loadData();
        }
        else {
            this.clearFilterDescriptors();
        }
    };
    RadListView.prototype.onSortingFunctionChanged = function (oldValue, newValue) {
        if (newValue) {
            this.loadData();
        }
        else {
            this.clearSortDescriptors();
        }
    };
    RadListView.prototype.subscribeForNativeScrollEvents = function () {
        ensureOnNativeScrollListener();
        this._scrollStateListener = new OnNativeScrollListenerClass(this);
        this._android.addOnScrollListener(this._scrollStateListener);
    };
    RadListView.prototype.bindingContextChanged = function (data) {
        if (this._headerView) {
            this._headerView.bindingContext = data.value;
        }
        if (this._footerView) {
            this._footerView.bindingContext = data.value;
        }
    };
    RadListView.prototype.refresh = function () {
        this.loadData();
    };
    RadListView.prototype.notifyPullToRefreshFinished = function (enableLoadOnDemand) {
        if (!this._pullToRefreshBehavior) {
            return;
        }
        if (!this._android) {
            return;
        }
        if (enableLoadOnDemand) {
            this._returnLoadOnDemandMode();
        }
        this._android.getAdapter().notifyRefreshFinished();
    };
    RadListView.prototype.notifyLoadOnDemandFinished = function (disableLoadOnDemand) {
        if (!this._loadOnDemandBehavior) {
            return;
        }
        if (!this._android) {
            return;
        }
        if (disableLoadOnDemand) {
            this._disableLoadOnDemand();
        }
        this._android.getAdapter().notifyLoadingFinished();
    };
    RadListView.prototype.notifySwipeToExecuteFinished = function () {
        if (this._swipeActionsBehavior) {
            this._swipeActionsBehavior.endExecute();
        }
        if (!this._swipeExecuteBehavior) {
            return;
        }
        if (!this._android) {
            return;
        }
        if (this._android.getAdapter()) {
            this._android.getAdapter().notifySwipeExecuteFinished();
        }
    };
    RadListView.prototype.retrieveNativeSnapMode = function (snapMode) {
        var nativeSnapMode = com.telerik.widget.list.SnappingSmoothScroller.SNAP_NONE;
        switch (snapMode.toLowerCase()) {
            case listViewCommonModule.ListViewItemSnapMode.Start.toLowerCase():
                nativeSnapMode = com.telerik.widget.list.SnappingSmoothScroller.SNAP_TOP;
                break;
            case listViewCommonModule.ListViewItemSnapMode.End.toLowerCase():
                nativeSnapMode = com.telerik.widget.list.SnappingSmoothScroller.SNAP_BOTTOM;
                break;
            case listViewCommonModule.ListViewItemSnapMode.Center.toLowerCase():
                nativeSnapMode = com.telerik.widget.list.SnappingSmoothScroller.SNAP_CENTER;
                break;
        }
        return nativeSnapMode;
    };
    RadListView.prototype.scrollToIndex = function (index, animate, snapMode) {
        if (animate === void 0) { animate = false; }
        if (snapMode === void 0) { snapMode = listViewCommonModule.ListViewItemSnapMode.Auto; }
        if (this._android) {
            var nativeSnapMode = this.retrieveNativeSnapMode(snapMode);
            if (!animate) {
                this._android.scrollToPosition(index, nativeSnapMode);
            }
            else {
                this._android.smoothScrollToPosition(index, nativeSnapMode);
            }
        }
    };
    RadListView.prototype.getScrollOffset = function () {
        if (!this._android) {
            return _super.prototype.getScrollOffset.call(this);
        }
        if (this.listViewLayout.scrollDirection === listViewCommonModule.ListViewScrollDirection.Vertical) {
            return utilsModule.layout.toDeviceIndependentPixels(this._android.computeVerticalScrollOffset());
        }
        else {
            return utilsModule.layout.toDeviceIndependentPixels(this._android.computeHorizontalScrollOffset());
        }
    };
    RadListView.prototype.scrollWithAmount = function (amount, animate) {
        if (this._android) {
            var layoutVertical = this.listViewLayout.scrollDirection === listViewCommonModule.ListViewScrollDirection.Vertical ? true : false;
            amount = utilsModule.layout.toDevicePixels(amount);
            if (layoutVertical) {
                if (animate) {
                    this._android.smoothScrollBy(0, amount);
                }
                else {
                    this._android.scrollBy(0, amount);
                }
            }
            else {
                if (animate) {
                    this._android.smoothScrollBy(amount, 0);
                }
                else {
                    this._android.scrollBy(amount, 0);
                }
            }
        }
    };
    RadListView.prototype.disposeViewHolderViews = function (views) {
        var _this = this;
        views.forEach(function (element) {
            if (!element.parent) {
                // TODO: investigate why this can happen
                return;
            }
            if (!(element.parent instanceof RadListView)) {
                _this._removeView(element.parent);
            }
            element.parent._removeView(element);
        });
    };
    RadListView.prototype._updateHeader = function () {
        var headerView = this.getViewForViewType(listViewCommonModule.ListViewViewTypes.HeaderView);
        this._android.setHeaderView(null);
        var layoutParams = this._getViewLayoutParams();
        if (headerView) {
            headerView.bindingContext = this.bindingContext;
            this.disposeViewHolderViews(this._headerViewHolderChildren);
            this._headerViewHolderChildren.push(headerView);
            this._addView(headerView);
            headerView.nativeView.setLayoutParams(layoutParams);
            this._android.setHeaderView(headerView.nativeView);
            this._headerView = headerView;
        }
    };
    RadListView.prototype._updateFooter = function () {
        var footerView = this.getViewForViewType(listViewCommonModule.ListViewViewTypes.FooterView);
        this._android.setFooterView(null);
        var layoutParams = this._getViewLayoutParams();
        if (footerView) {
            footerView.bindingContext = this.bindingContext;
            this.disposeViewHolderViews(this._footerViewHolderChildren);
            this._footerViewHolderChildren.push(footerView);
            this._addView(footerView);
            footerView.nativeView.setLayoutParams(layoutParams);
            this._android.setFooterView(footerView.nativeView);
            this._footerView = footerView;
        }
    };
    RadListView.prototype.updateSwipeActionsBehavior = function () {
        if (!this._android || !(this.itemSwipeTemplate || this.itemViewLoader)) {
            return;
        }
        if (this.swipeActions === true) {
            if (!this._swipeActionsBehavior) {
                this._swipeActionsBehavior = new com.telerik.widget.list.SwipeActionsBehavior();
                this._swipeActionsBehavior.setDockMode(com.telerik.widget.list.SwipeActionsBehavior.SwipeDockMode.DockAtLimit);
                this._android.addBehavior(this._swipeActionsBehavior);
                var that_1 = new WeakRef(this);
                var impl = {
                    swipeLimits: { left: that_1.get().getMeasuredWidth(), top: that_1.get().getMeasuredHeight(), right: that_1.get().getMeasuredWidth(), bottom: that_1.get().getMeasuredHeight(), threshold: 0 },
                    onSwipeStarted: function (event) {
                        var owner = that_1.get();
                        var originalPosition = owner._getOriginalIndex(event.swipedItemPosition());
                        var swipeView = owner._listViewAdapter.getSwipeViewForItem(owner.getItemAtIndex(originalPosition));
                        var mainView = owner._listViewAdapter.getViewForItem(owner.getItemAtIndex(originalPosition));
                        var args = {
                            eventName: listViewCommonModule.RadListView.itemSwipeProgressStartedEvent,
                            object: that_1.get(),
                            swipeView: swipeView,
                            mainView: mainView,
                            index: originalPosition,
                            data: { swipeLimits: this.swipeLimits }
                        };
                        that_1.get().notify(args);
                        var listView = that_1.get();
                        if (listView.listViewLayout.scrollDirection === listViewCommonModule.ListViewScrollDirection.Horizontal) {
                            if (this.swipeLimits.top >= 0) {
                                that_1.get()._swipeActionsBehavior.setSwipeLimitStart(this.swipeLimits.top);
                            }
                            if (this.swipeLimits.bottom >= 0) {
                                that_1.get()._swipeActionsBehavior.setSwipeLimitEnd(this.swipeLimits.bottom);
                            }
                        }
                        else {
                            if (this.swipeLimits.left >= 0) {
                                that_1.get()._swipeActionsBehavior.setSwipeLimitStart(this.swipeLimits.left);
                            }
                            if (this.swipeLimits.right >= 0) {
                                that_1.get()._swipeActionsBehavior.setSwipeLimitEnd(this.swipeLimits.right);
                            }
                        }
                        if (this.swipeLimits.threshold !== undefined) {
                            that_1.get()._swipeActionsBehavior.setSwipeThresholdEnd(this.swipeLimits.threshold);
                            that_1.get()._swipeActionsBehavior.setSwipeThresholdStart(this.swipeLimits.threshold);
                        }
                    },
                    onSwipeProgressChanged: function (event) {
                        var owner = that_1.get();
                        var originalPosition = owner._getOriginalIndex(event.swipedItemPosition());
                        var swipeView = owner._listViewAdapter.getSwipeViewForItem(owner.getItemAtIndex(originalPosition));
                        var mainView = owner._listViewAdapter.getViewForItem(owner.getItemAtIndex(originalPosition));
                        var args = {
                            eventName: listViewCommonModule.RadListView.itemSwipeProgressChangedEvent,
                            object: owner,
                            swipeView: swipeView,
                            mainView: mainView,
                            index: originalPosition,
                            data: {
                                x: owner.listViewLayout.scrollDirection === "Vertical" ? event.currentOffset() : 0,
                                y: owner.listViewLayout.scrollDirection === "Vertical" ? 0 : event.currentOffset(),
                                swipeLimits: this.swipeLimits
                            }
                        };
                        owner.notify(args);
                    },
                    onSwipeEnded: function (event) {
                    },
                    onExecuteFinished: function (event) {
                        var owner = that_1.get();
                        var originalPosition = owner._getOriginalIndex(event.swipedItemPosition());
                        var swipeView = owner._listViewAdapter.getSwipeViewForItem(owner.getItemAtIndex(originalPosition));
                        var mainView = owner._listViewAdapter.getViewForItem(owner.getItemAtIndex(originalPosition));
                        var args = {
                            eventName: listViewCommonModule.RadListView.itemSwipeProgressEndedEvent,
                            object: owner,
                            swipeView: swipeView,
                            mainView: mainView,
                            index: originalPosition,
                            data: {
                                x: owner.listViewLayout.scrollDirection === "Vertical" ? event.swipePositionWhenReleased() : 0,
                                y: owner.listViewLayout.scrollDirection === "Vertical" ? 0 : event.swipePositionWhenReleased(),
                                swipeLimits: this.swipeLimits
                            }
                        };
                        owner.notify(args);
                    },
                    onSwipeStateChanged: function (oldState, newState) {
                    },
                };
                this._swipeActionsListener = new com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsListener(impl);
                this._swipeActionsBehavior.addListener(this._swipeActionsListener);
            }
        }
        else {
            if (this._swipeActionsBehavior) {
                this._android.removeBehavior(this._swipeActionsBehavior);
                this._swipeActionsBehavior.removeListener(this._swipeActionsListener);
            }
        }
    };
    // TODO: This should be deprecated and removed
    RadListView.prototype.updateSwipeToExecuteBehavior = function () {
        if (!this._android || !(this.itemSwipeTemplate || this.itemViewLoader)) {
            return;
        }
        if (this.itemSwipe === true) {
            if (!this._swipeExecuteBehavior) {
                this._swipeExecuteBehavior = new com.telerik.widget.list.SwipeExecuteBehavior();
                this._swipeExecuteBehavior.setAutoDissolve(false);
                this._android.addBehavior(this._swipeExecuteBehavior);
                var that_2 = new WeakRef(this);
                var impl = {
                    swipeLimits: (that_2.get().listViewLayout.scrollDirection === "Vertical") ?
                        { left: 150, top: 0, right: 150, bottom: 0, threshold: 75 } :
                        { left: 0, top: 150, right: 0, bottom: 150, threshold: 75 },
                    onSwipeStarted: function (position) {
                        var args = {
                            eventName: listViewCommonModule.RadListView.itemSwipeProgressStartedEvent,
                            object: that_2.get(),
                            swipeView: that_2.get()._listViewAdapter.getSwipeViewForItem(that_2.get().getItemAtIndex(position)),
                            index: position,
                            groupIndex: -1,
                            data: { swipeLimits: this.swipeLimits }
                        };
                        that_2.get().notify(args);
                        var listView = that_2.get();
                        if (listView.listViewLayout.scrollDirection === listViewCommonModule.ListViewScrollDirection.Horizontal) {
                            that_2.get()._swipeExecuteBehavior.setSwipeLimitStart(-this.swipeLimits.top);
                            that_2.get()._swipeExecuteBehavior.setSwipeLimitEnd(this.swipeLimits.bottom);
                        }
                        else {
                            that_2.get()._swipeExecuteBehavior.setSwipeLimitStart(-this.swipeLimits.right);
                            that_2.get()._swipeExecuteBehavior.setSwipeLimitEnd(this.swipeLimits.left);
                        }
                    },
                    onSwipeProgressChanged: function (position, currentOffset, swipeContent) {
                        var args = {
                            eventName: listViewCommonModule.RadListView.itemSwipeProgressChangedEvent,
                            object: that_2.get(),
                            swipeView: that_2.get()._listViewAdapter.getSwipeViewForItem(that_2.get().getItemAtIndex(position)),
                            index: position,
                            data: { x: currentOffset, y: 0, swipeLimits: this.swipeLimits },
                            returnValue: undefined
                        };
                        that_2.get().notify(args);
                    },
                    onSwipeEnded: function (position, finalOffset) {
                        var args = {
                            eventName: listViewCommonModule.RadListView.itemSwipeProgressEndedEvent,
                            object: that_2.get(),
                            swipeView: that_2.get()._listViewAdapter.getSwipeViewForItem(that_2.get().getItemAtIndex(position)),
                            index: position,
                            data: { x: finalOffset, y: 0, swipeLimits: this.swipeLimits },
                            returnValue: undefined
                        };
                        that_2.get().notify(args);
                        if (args.data.swipeLimits) {
                            if (Math.abs(finalOffset) > args.data.swipeLimits.threshold) {
                                if (finalOffset < 0) {
                                    if (that_2.get().listViewLayout.scrollDirection === "Horizontal") {
                                        that_2.get()._swipeExecuteBehavior.setSwipeOffset(-args.data.swipeLimits.bottom);
                                    }
                                    else if (that_2.get().listViewLayout.scrollDirection === "Vertical") {
                                        that_2.get()._swipeExecuteBehavior.setSwipeOffset(-args.data.swipeLimits.right);
                                    }
                                }
                                else if (finalOffset > 0) {
                                    if (that_2.get().listViewLayout.scrollDirection === "Horizontal") {
                                        that_2.get()._swipeExecuteBehavior.setSwipeOffset(args.data.swipeLimits.top);
                                    }
                                    else if (that_2.get().listViewLayout.scrollDirection === "Vertical") {
                                        that_2.get()._swipeExecuteBehavior.setSwipeOffset(args.data.swipeLimits.left);
                                    }
                                }
                            }
                            else {
                                that_2.get()._swipeExecuteBehavior.setSwipeOffset(0);
                            }
                        }
                    },
                    onExecuteFinished: function (position) {
                    }
                };
                this._swipeExecuteListener = new com.telerik.widget.list.SwipeExecuteBehavior.SwipeExecuteListener(impl);
                this._swipeExecuteBehavior.addListener(this._swipeExecuteListener);
            }
        }
        else {
            if (this._swipeExecuteBehavior) {
                this._android.removeBehavior(this._swipeExecuteBehavior);
                this._swipeExecuteBehavior.removeListener(this._swipeExecuteListener);
                this._swipeExecuteBehavior = null;
                this._swipeExecuteListener = null;
            }
        }
    };
    RadListView.prototype.updatePullToRefreshBehavior = function () {
        if (!this._android) {
            return;
        }
        if (this.pullToRefresh === true) {
            if (!this._pullToRefreshBehavior) {
                this._pullToRefreshBehavior = new com.telerik.widget.list.SwipeRefreshBehavior();
                this._android.addBehavior(this._pullToRefreshBehavior);
                var that_3 = new WeakRef(this);
                this._pullToRefreshBehavior.addListener(new com.telerik.widget.list.SwipeRefreshBehavior.SwipeRefreshListener({
                    onRefreshRequested: function () {
                        var args = {
                            eventName: listViewCommonModule.RadListView.pullToRefreshInitiatedEvent,
                            object: that_3.get(),
                            returnValue: true
                        };
                        that_3.get().notify(args);
                    }
                }));
            }
            if (this._pullToRefreshBehavior && this.pullToRefreshStyle !== undefined) {
                var style = this.pullToRefreshStyle;
                if (style.indicatorColor) {
                    var colorsArray = new Array();
                    colorsArray.push(new color_1.Color(style.indicatorColor).android);
                    this._pullToRefreshBehavior.swipeRefresh().setColorSchemeColors(colorsArray);
                }
                if (style.indicatorBackgroundColor) {
                    this._pullToRefreshBehavior.swipeRefresh().setProgressBackgroundColorSchemeColor(new color_1.Color(style.indicatorBackgroundColor).android);
                }
            }
        }
        else {
            if (this._pullToRefreshBehavior) {
                this._android.removeBehavior(this._pullToRefreshBehavior);
                this._pullToRefreshBehavior = null;
            }
        }
    };
    RadListView.prototype.updateCollapsibleGroupsBehavior = function () {
        if (!this._android || !this.enableCollapsibleGroups) {
            return;
        }
        if (this.enableCollapsibleGroups) {
            if (!this._collapsibleGroupsBehavior) {
                this._collapsibleGroupsBehavior = new com.telerik.widget.list.CollapsibleGroupsBehavior();
                this._android.addBehavior(this._collapsibleGroupsBehavior);
            }
        }
        else {
            if (this._collapsibleGroupsBehavior) {
                this._android.removeBehavior(this._collapsibleGroupsBehavior);
                this._collapsibleGroupsBehavior = null;
            }
        }
    };
    RadListView.prototype.setLoadOnDemandModeInternal = function (value) {
        this._loadOnDemandModeInternal = value;
        this.updateLoadOnDemandBehavior();
    };
    RadListView.prototype.updateLoadOnDemandBehavior = function () {
        if (!this._android) {
            return;
        }
        if (!this._loadOnDemandBehavior) {
            this._loadOnDemandBehavior = undefined;
            var loadOnDemandView = this.getViewForViewType(listViewCommonModule.ListViewViewTypes.LoadOnDemandView);
            if (loadOnDemandView) {
                this.disposeViewHolderViews(this._loadOnDemandViewHolderChildren);
                this._loadOnDemandViewHolderChildren.push(loadOnDemandView);
                this._addView(loadOnDemandView);
                switch (this._loadOnDemandModeInternal) {
                    case listViewCommonModule.ListViewLoadOnDemandMode.Manual:
                        this._loadOnDemandBehavior = new com.telerik.widget.list.LoadOnDemandBehavior(loadOnDemandView.nativeView, new android.widget.LinearLayout(this._context));
                        break;
                    case listViewCommonModule.ListViewLoadOnDemandMode.Auto:
                    default: {
                        this._loadOnDemandBehavior = new com.telerik.widget.list.LoadOnDemandBehavior(new android.widget.LinearLayout(this._context), loadOnDemandView.nativeView);
                        break;
                    }
                }
            }
            else {
                this._loadOnDemandBehavior = new com.telerik.widget.list.LoadOnDemandBehavior();
            }
            this._android.addBehavior(this._loadOnDemandBehavior);
            var that_4 = new WeakRef(this);
            this._loadOnDemandBehavior.addListener(new com.telerik.widget.list.LoadOnDemandBehavior.LoadOnDemandListener({
                onLoadStarted: function () {
                    var args = {
                        eventName: listViewCommonModule.RadListView.loadMoreDataRequestedEvent,
                        object: that_4.get(),
                        returnValue: true
                    };
                    that_4.get().notify(args);
                },
                onLoadFinished: function () {
                }
            }));
        }
        if (!isNaN(this.loadOnDemandBufferSize)) {
            this._loadOnDemandBehavior.setMaxRemainingItems(this.loadOnDemandBufferSize);
        }
        switch (this._loadOnDemandModeInternal) {
            case listViewCommonModule.ListViewLoadOnDemandMode.Manual:
                this._loadOnDemandBehavior.setEnabled(true);
                this._loadOnDemandBehavior.setMode(com.telerik.widget.list.LoadOnDemandBehavior.LoadOnDemandMode.MANUAL);
                break;
            case listViewCommonModule.ListViewLoadOnDemandMode.Auto:
                this._loadOnDemandBehavior.setEnabled(true);
                this._loadOnDemandBehavior.setMode(com.telerik.widget.list.LoadOnDemandBehavior.LoadOnDemandMode.AUTOMATIC);
                break;
            default: {
                this._loadOnDemandBehavior.setEnabled(false);
                break;
            }
        }
    };
    RadListView.prototype.updateReorderBehavior = function () {
        if (!this._android) {
            return;
        }
        if (this.itemReorder) {
            if (!this._reorderBehavior) {
                ensureExtendedReorderWithHandlesBehavior();
                this._reorderBehavior = (this.reorderMode.toLowerCase() === listViewCommonModule.ListViewReorderMode.HoldAndDrag) ?
                    new com.telerik.widget.list.ItemReorderBehavior() :
                    new ExtendedReorderWithHandlesBehaviorClass(-1);
                this._reorderBehavior['nsOwner'] = this;
                this._android.addBehavior(this._reorderBehavior);
                var that_5 = new WeakRef(this);
                var impl = {
                    newIndex: -1,
                    oldIndex: -1,
                    onReorderStarted: function (position) {
                        this.oldIndex = position;
                        var view = that_5.get().getViewForItem(that_5.get().getItemAtIndex(position));
                        var args = {
                            eventName: listViewCommonModule.RadListView.itemReorderStartedEvent,
                            object: that_5.get(),
                            index: this.oldIndex,
                            groupIndex: -1,
                            view: view
                        };
                        that_5.get().notify(args);
                    },
                    onReorderItem: function (fromIndex, toIndex) {
                        this.newIndex = toIndex;
                    },
                    onReorderFinished: function () {
                        if (this.newIndex === -1) {
                            this.newIndex = this.oldIndex;
                        }
                        var view = that_5.get().getViewForItem(that_5.get().getItemAtIndex(this.newIndex));
                        var args = {
                            eventName: listViewCommonModule.RadListView.itemReorderedEvent,
                            object: that_5.get(),
                            index: this.oldIndex,
                            groupIndex: -1,
                            data: { targetIndex: this.newIndex, targetGroupIndex: -1 },
                            view: view
                        };
                        this.newIndex = -1;
                        that_5.get().notify(args);
                    }
                };
                this._reorderBehavior.addListener(new com.telerik.widget.list.ItemReorderBehavior.ItemReorderListener(impl));
            }
        }
        else {
            if (this._reorderBehavior) {
                this._android.removeBehavior(this._reorderBehavior);
                this._reorderBehavior = undefined;
            }
        }
    };
    RadListView.prototype.updateSelectionBehavior = function () {
        if (!this._android) {
            return;
        }
        if (!this._selectionBehavior) {
            this._selectionBehavior = new com.telerik.widget.list.SelectionBehavior();
            this._android.addBehavior(this._selectionBehavior);
            var that_6 = new WeakRef(this);
            this._selectionBehavior.addListener(new com.telerik.widget.list.SelectionBehavior.SelectionChangedListener({
                onSelectionStarted: function () {
                },
                onItemIsSelectedChanged: function (position, newValue) {
                    var currentEventName = newValue === true ? listViewCommonModule.RadListView.itemSelectedEvent : listViewCommonModule.RadListView.itemDeselectedEvent;
                    var listView = that_6.get();
                    var isGroupHeader = listView._listViewAdapter.isGroupHeader(position);
                    if (!isGroupHeader) {
                        var listView_1 = that_6.get();
                        var originalPosition = listView_1._getOriginalIndex(position);
                        var item = listView_1.getItemAtIndex(originalPosition);
                        var view = listView_1.getViewForItem(item);
                        var args = {
                            eventName: currentEventName,
                            object: listView_1,
                            index: originalPosition,
                            groupIndex: -1,
                            view: view
                        };
                        listView_1.notify(args);
                    }
                },
                onSelectionEnded: function () {
                }
            }));
        }
        if (this.multipleSelection) {
            this._selectionBehavior.setSelectionMode(com.telerik.widget.list.SelectionBehavior.SelectionMode.MULTIPLE);
        }
        else {
            this._selectionBehavior.setSelectionMode(com.telerik.widget.list.SelectionBehavior.SelectionMode.SINGLE);
        }
        switch (this.selectionBehavior) {
            case listViewCommonModule.ListViewSelectionBehavior.None:
                this._android.removeBehavior(this._selectionBehavior);
                this._selectionBehavior = undefined;
                break;
            case listViewCommonModule.ListViewSelectionBehavior.LongPress:
                this._selectionBehavior.setSelectionOnTouch(com.telerik.widget.list.SelectionBehavior.SelectionOnTouch.NEVER);
                break;
            default: {
                this._selectionBehavior.setSelectionOnTouch(com.telerik.widget.list.SelectionBehavior.SelectionOnTouch.ALWAYS);
            }
        }
    };
    RadListView.prototype.clearFilterDescriptors = function () {
        if (!this._listViewAdapter) {
            return;
        }
        this._listViewAdapter.clearFilterDescriptors();
    };
    RadListView.prototype.clearGroupDescriptors = function () {
        if (!this._listViewAdapter) {
            return;
        }
        this._listViewAdapter.clearGroupDescriptors();
    };
    RadListView.prototype.clearSortDescriptors = function () {
        if (!this._listViewAdapter) {
            return;
        }
        this._listViewAdapter.clearSortDescriptors();
    };
    RadListView.prototype.loadData = function () {
        if (!this.items || !this._android) {
            return;
        }
        var nativeSource = new java.util.ArrayList();
        var dsLength = this.items.length;
        this._resetCurrentId();
        for (var i = 0; i < dsLength; i++) {
            var javaObject = new java.lang.Integer(this._getUniqueItemId());
            nativeSource.add(javaObject);
        }
        if (this._listViewAdapter) {
            this._listViewAdapter.disposeViewHolderViews();
        }
        if (!this.isDataOperationsEnabled) {
            this._listViewAdapter = new ListViewAdapterClass(nativeSource, this);
        }
        else {
            this._listViewAdapter = new ListViewDataSourceAdapterClass(nativeSource, this);
        }
        if (this.isDataOperationsEnabled) {
            var that_7 = this;
            if (that_7.groupingFunction) {
                this._listViewAdapter.addGroupDescriptor(new com.telerik.android.common.Function({
                    apply: function (object) {
                        var item = that_7.getItemAtIndex(object);
                        return that_7.groupingFunction(item);
                    }
                }));
            }
            if (that_7.filteringFunction) {
                this._listViewAdapter.addFilterDescriptor(new com.telerik.android.common.Function({
                    apply: function (object) {
                        var item = that_7.getItemAtIndex(object);
                        return (that_7.filteringFunction(item));
                    }
                }));
            }
            if (that_7.sortingFunction) {
                this._listViewAdapter.addSortDescriptor(new com.telerik.android.common.Function2({
                    apply: function (object, object2) {
                        var previousItem = that_7.getItemAtIndex(object);
                        var nextItem = that_7.getItemAtIndex(object2);
                        var javaRes = that_7.sortingFunction(nextItem, previousItem);
                        return new java.lang.Integer(javaRes);
                    }
                }));
            }
        }
        this._android.setAdapter(this._listViewAdapter);
        var args = {
            eventName: listViewCommonModule.RadListView.dataPopulatedEvent,
            object: this
        };
        this.notify(args);
    };
    RadListView.prototype._disableLoadOnDemand = function () {
        this.setLoadOnDemandModeInternal(listViewCommonModule.ListViewLoadOnDemandMode.None);
    };
    // TODO: This can be used for https://github.com/telerik/nativescript-ui-feedback/issues/790
    RadListView.prototype._returnLoadOnDemandMode = function () {
        this.setLoadOnDemandModeInternal(this.loadOnDemandMode);
    };
    // Returns the original index while taking into account if grouping, filtering and/or sorting is enabled.
    RadListView.prototype._getOriginalIndex = function (inputIndex) {
        return this.isDataOperationsEnabled ? this._listViewAdapter.getItemId(inputIndex) : inputIndex;
    };
    return RadListView;
}(listViewCommonModule.RadListView));
exports.RadListView = RadListView;
var AndroidLVLayoutBase = /** @class */ (function (_super) {
    __extends(AndroidLVLayoutBase, _super);
    function AndroidLVLayoutBase() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Object.defineProperty(AndroidLVLayoutBase.prototype, "android", {
        get: function () {
            return this._android;
        },
        enumerable: true,
        configurable: true
    });
    AndroidLVLayoutBase.prototype._init = function (owner) {
        this._owner = new WeakRef(owner);
        if (this._owner.get()._android) {
            this._onOwnerUICreated();
        }
    };
    AndroidLVLayoutBase.prototype._reset = function () {
    };
    AndroidLVLayoutBase.prototype._onOwnerUICreated = function () {
        this._android = this.getLayoutManager();
        var owner = this._owner.get();
        owner._android.setLayoutManager(this._android);
        if (this.scrollDirection) {
            this.setLayoutOrientation(this.scrollDirection);
        }
        if (this.itemInsertAnimation) {
            this.updateItemAnimator(this.itemInsertAnimation);
        }
        if (this.itemDeleteAnimation) {
            this.updateItemAnimator(this.itemDeleteAnimation);
        }
    };
    AndroidLVLayoutBase.prototype.reset = function () {
        this._owner.get()._android.setLayoutManager(null);
        this._owner = null;
    };
    AndroidLVLayoutBase.prototype.getLayoutManager = function () {
        return undefined;
    };
    AndroidLVLayoutBase.prototype.onScrollDirectionChanged = function (oldValue, newValue) {
        if (newValue && this._android) {
            this.setLayoutOrientation(newValue);
        }
    };
    AndroidLVLayoutBase.prototype.onItemInsertAnimationChanged = function (oldValue, newValue) {
        if (this._owner) {
            this.updateItemAnimator(newValue);
        }
    };
    AndroidLVLayoutBase.prototype.onItemDeleteAnimationChanged = function (oldValue, newValue) {
        if (this._owner) {
            this.updateItemAnimator(newValue);
        }
    };
    AndroidLVLayoutBase.prototype.setLayoutOrientation = function (orientation) {
        this._android.setOrientation((orientation === listViewCommonModule.ListViewScrollDirection.Horizontal) ?
            android.support.v7.widget.LinearLayoutManager.HORIZONTAL :
            android.support.v7.widget.LinearLayoutManager.VERTICAL);
    };
    AndroidLVLayoutBase.prototype.updateItemAnimator = function (newAnimator) {
        var owner = this._owner.get();
        if (!newAnimator) {
            owner._android.setItemAnimator(null);
            return;
        }
        switch (listViewCommonModule.ListViewItemAnimation[newAnimator]) {
            case listViewCommonModule.ListViewItemAnimation.Fade: {
                owner._android.setItemAnimator(new com.telerik.widget.list.FadeItemAnimator());
                break;
            }
            case listViewCommonModule.ListViewItemAnimation.Scale: {
                owner._android.setItemAnimator(new com.telerik.widget.list.ScaleItemAnimator());
                break;
            }
            case listViewCommonModule.ListViewItemAnimation.Slide: {
                owner._android.setItemAnimator(new com.telerik.widget.list.SlideItemAnimator());
                break;
            }
            default:
                owner._android.setItemAnimator(null);
        }
    };
    return AndroidLVLayoutBase;
}(listViewCommonModule.ListViewLayoutBase));
exports.AndroidLVLayoutBase = AndroidLVLayoutBase;
var ListViewLinearLayout = /** @class */ (function (_super) {
    __extends(ListViewLinearLayout, _super);
    function ListViewLinearLayout() {
        return _super.call(this) || this;
    }
    ListViewLinearLayout.prototype.getLayoutManager = function () {
        return new android.support.v7.widget.LinearLayoutManager(this._owner.get()._context);
    };
    return ListViewLinearLayout;
}(AndroidLVLayoutBase));
exports.ListViewLinearLayout = ListViewLinearLayout;
var ListViewGridLayout = /** @class */ (function (_super) {
    __extends(ListViewGridLayout, _super);
    function ListViewGridLayout() {
        return _super.call(this) || this;
    }
    ListViewGridLayout.prototype.onSpanCountPropertyChanged = function (oldValue, newValue) {
        this.onSpanCountChanged(oldValue, newValue);
    };
    ListViewGridLayout.prototype.onSpanCountChanged = function (oldValue, newValue) {
        if (!isNaN(+newValue) && this.android) {
            this.android.setSpanCount(newValue);
        }
    };
    ListViewGridLayout.prototype.onItemHeightChanged = function (oldValue, newValue) {
        console.log("Warning: Setting the 'itemHeight' property of 'ListViewGridLayout' is not supported by the Android platform.");
    };
    ListViewGridLayout.prototype.onItemWidthChanged = function (oldValue, newValue) {
        console.log("Warning: Setting the 'itemWidth' property of 'ListViewGridLayout' is not supported by the Android platform.");
    };
    ListViewGridLayout.prototype.getLayoutManager = function () {
        this.spanCount = (this.spanCount ? this.spanCount : 2);
        return new android.support.v7.widget.GridLayoutManager(this._owner.get()._context, this.spanCount);
    };
    // NOTE: this property should be defined in common module, but inheritance will not be possible then
    ListViewGridLayout.spanCountProperty = new view_1.Property({
        name: "spanCount",
        defaultValue: undefined,
        valueConverter: parseInt,
        valueChanged: function (target, oldValue, newValue) {
            target.onSpanCountPropertyChanged(oldValue, newValue);
        },
    });
    return ListViewGridLayout;
}(ListViewLinearLayout));
exports.ListViewGridLayout = ListViewGridLayout;
ListViewGridLayout.spanCountProperty.register(ListViewGridLayout);
var ListViewStaggeredLayout = /** @class */ (function (_super) {
    __extends(ListViewStaggeredLayout, _super);
    function ListViewStaggeredLayout() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ListViewStaggeredLayout.prototype.getLayoutManager = function () {
        var orientation = this.scrollDirection === listViewCommonModule.ListViewScrollDirection.Vertical ?
            android.support.v7.widget.StaggeredGridLayoutManager.VERTICAL : android.support.v7.widget.StaggeredGridLayoutManager.HORIZONTAL;
        this.spanCount = (this.spanCount ? this.spanCount : 2);
        return new android.support.v7.widget.StaggeredGridLayoutManager(this.spanCount, orientation);
    };
    return ListViewStaggeredLayout;
}(ListViewGridLayout));
exports.ListViewStaggeredLayout = ListViewStaggeredLayout;
var OnNativeScrollListenerClass;
function ensureOnNativeScrollListener() {
    if (OnNativeScrollListenerClass) {
        return;
    }
    var OnNativeScrollListener = /** @class */ (function (_super) {
        __extends(OnNativeScrollListener, _super);
        function OnNativeScrollListener(owner) {
            var _this = _super.call(this) || this;
            _this._wasIdle = true;
            _this._wasDragging = false;
            _this._owner = new WeakRef(owner);
            return global.__native(_this);
        }
        OnNativeScrollListener.prototype.onScrolled = function (param0, param1, param2) {
            var owner = this._owner.get();
            var eventData = {
                eventName: listViewCommonModule.RadListView.scrolledEvent,
                object: owner,
                scrollOffset: owner.getScrollOffset()
            };
            owner.notify(eventData);
        };
        OnNativeScrollListener.prototype.onScrollStateChanged = function (param0, scrollState) {
            var owner = this._owner.get();
            var eventData;
            switch (scrollState) {
                case android.support.v7.widget.RecyclerView.SCROLL_STATE_IDLE:
                    if (this._wasDragging) {
                        eventData = {
                            eventName: listViewCommonModule.RadListView.scrollDragEndedEvent,
                            object: owner,
                            scrollOffset: owner.getScrollOffset()
                        };
                        this._wasDragging = false;
                        if (owner.hasListeners(eventData.eventName)) {
                            owner.notify(eventData);
                        }
                    }
                    eventData = {
                        eventName: listViewCommonModule.RadListView.scrollEndedEvent,
                        object: owner,
                        scrollOffset: owner.getScrollOffset()
                    };
                    this._wasIdle = true;
                    break;
                case android.support.v7.widget.RecyclerView.SCROLL_STATE_DRAGGING:
                    this._wasDragging = true;
                    eventData = {
                        eventName: this._wasIdle ? listViewCommonModule.RadListView.scrollStartedEvent : listViewCommonModule.RadListView.scrolledEvent,
                        object: owner,
                        scrollOffset: owner.getScrollOffset()
                    };
                    this._wasIdle = false;
                    break;
                case android.support.v7.widget.RecyclerView.SCROLL_STATE_SETTLING:
                    if (this._wasDragging) {
                        eventData = {
                            eventName: listViewCommonModule.RadListView.scrollDragEndedEvent,
                            object: owner,
                            scrollOffset: owner.getScrollOffset()
                        };
                        this._wasDragging = false;
                        if (owner.hasListeners(eventData.eventName)) {
                            owner.notify(eventData);
                        }
                    }
                    eventData = {
                        eventName: listViewCommonModule.RadListView.scrolledEvent,
                        object: owner,
                        scrollOffset: owner.getScrollOffset()
                    };
                    break;
            }
            if (owner.hasListeners(eventData.eventName)) {
                owner.notify(eventData);
            }
        };
        return OnNativeScrollListener;
    }(android.support.v7.widget.RecyclerView.OnScrollListener));
    OnNativeScrollListenerClass = OnNativeScrollListener;
}
