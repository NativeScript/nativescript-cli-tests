export * from "./ui-listview.common";
import * as viewModule from "tns-core-modules/ui/core/view";
import * as commonModule from "./ui-listview.common";
import { KeyedTemplate } from "tns-core-modules/ui/core/view";
import { PropertyChangeData } from "tns-core-modules/data/observable";
export declare namespace knownTemplates {
    let itemTemplate: string;
    let itemSwipeTemplate: string;
    let loadOnDemandItemTemplate: string;
    let headerItemTemplate: string;
    let footerItemTemplate: string;
    let groupTemplate: string;
}
export declare namespace knownMultiTemplates {
    const itemTemplates = "itemTemplates";
}
export declare class ReorderHandle extends commonModule.ReorderHandle {
    constructor();
}
export declare class ListViewLayoutBase extends commonModule.ListViewLayoutBase {
    private _ios;
    protected _owner: WeakRef<RadListView>;
    readonly ios: any;
    protected supportsDynamicSize(): boolean;
    init(owner: WeakRef<RadListView>): void;
    reset(): void;
    protected getNativeLayout(): any;
    protected onScrollDirectionChanged(oldValue: string, newValue: string): void;
    private syncOwnerScrollDirection(newScrollDirection);
    protected onItemInsertAnimationChanged(oldValue: string, newValue: string): void;
    protected onItemDeleteAnimationChanged(oldValue: string, newValue: string): void;
    protected onItemWidthChanged(oldValue: number, newValue: number): void;
    protected onItemHeightChanged(oldValue: number, newValue: number): void;
    private updateIsDynamicSize();
    protected updateItemSize(): void;
}
export declare class ListViewLinearLayout extends ListViewLayoutBase {
    protected getNativeLayout(): TKListViewLinearLayout;
}
export declare class ListViewGridLayout extends ListViewLayoutBase {
    spanCount: number;
    lineSpacing: number;
    protected getNativeLayout(): TKListViewGridLayout;
    protected supportsDynamicSize(): boolean;
    static spanCountProperty: viewModule.Property<ListViewGridLayout, number>;
    private onSpanCountPropertyChanged(oldValue, newValue);
    protected onSpanCountChanged(oldValue: number, newValue: number): void;
    static lineSpacingProperty: viewModule.Property<ListViewGridLayout, number>;
    private onLineSpacingPropertyChanged(oldValue, newValue);
    protected onLineSpacingChanged(oldValue: number, newValue: number): void;
}
export declare class ListViewStaggeredLayout extends ListViewGridLayout {
    protected getNativeLayout(): TKListViewStaggeredLayout;
    protected supportsDynamicSize(): boolean;
    protected updateItemSize(): void;
}
export declare class ExtendedLoadOnDemandCell extends TKListViewLoadOnDemandCell {
    private _view;
    static new(): ExtendedLoadOnDemandCell;
    static class(): any;
    systemLayoutSizeFittingSize(targetSize: any): CGSize;
    willMoveToSuperview(newSuperview: UIView): void;
    view: viewModule.View;
}
export declare class ExtendedListViewCell extends TKListViewCell {
    private touchStarted;
    static new(): ExtendedListViewCell;
    static class(): any;
    willMoveToSuperview(newSuperview: UIView): void;
    systemLayoutSizeFittingSize(targetSize: any): any;
    touchesBeganWithEvent(touches: NSSet<any>, event: any): void;
    touchesMovedWithEvent(touches: NSSet<any>, event: any): void;
    touchesEndedWithEvent(touches: NSSet<any>, event: any): void;
    getCurrentIndexPath(): NSIndexPath;
    private getIndexForIndexPath(owner, indexPath);
    myContentView: viewModule.View;
    myBackgroundView: viewModule.View;
    itemViewMeasuredSize: any;
    swipeViewMeasuredSize: any;
    view: any;
}
export declare class RadListView extends commonModule.RadListView {
    private _delegate;
    private _dataSource;
    private _heights;
    _realizedCells: Map<number, ExtendedListViewCell>;
    private _nextCellTag;
    private _isDataDirty;
    _preparingCell: any;
    private _ios;
    _shouldDisableLoadOnDemand: boolean;
    _shouldReEnableLoadOnDemand: boolean;
    _insertingItemsWithAnimation: boolean;
    readonly _nativeView: TKListView;
    constructor();
    private reloadDataSource();
    createNativeView(): TKListView;
    disposeNativeView(): void;
    private setHeightForCell(index, value);
    selectAll(): void;
    deselectAll(): void;
    isItemSelected(item: any): boolean;
    selectItemAt(index: number): void;
    deselectItemAt(index: number): void;
    getViewForItem(item: any): viewModule.View;
    getSelectedItems(): Array<any>;
    bindingContextChanged(data: PropertyChangeData): void;
    updateHeaderFooter(): void;
    protected onReorderModeChanged(oldValue: string, newValue: string): void;
    protected onListViewLayoutChanged(oldValue: ListViewLayoutBase, newValue: ListViewLayoutBase): void;
    protected onItemTemplateSelectorChanged(oldValue: string | ((item: any, index: number, items: any) => string), newValue: string | ((item: any, index: number, items: any) => string)): void;
    private syncListViewLayout(newValue);
    private clearRealizedCells();
    private _clearCellViews(cell);
    protected onItemTemplateChanged(oldValue: string, newValue: string): void;
    protected onGroupTemplateChanged(oldValue: string, newValue: string): void;
    protected onItemTemplatesChanged(oldValue: string | Array<KeyedTemplate>, newValue: string | Array<KeyedTemplate>): void;
    protected onLoadOnDemandItemTemplateChanged(oldValue: string, newValue: string): void;
    protected onItemSwipeTemplateChanged(oldValue: string, newValue: string): void;
    protected onMultipleSelectionChanged(oldValue: boolean, newValue: boolean): void;
    protected onHeaderItemTemplateChanged(oldValue: string, newValue: string): void;
    protected onFooterItemTemplateChanged(oldValue: string, newValue: string): void;
    protected onEnableCollapsibleGroupsChanged(oldValue: boolean, newValue: boolean): void;
    protected onGroupingFunctionChanged(oldValue: (item: any) => any, newValue: (item: any) => any): void;
    protected onFilteringFunctionChanged(oldValue: (item: any) => boolean, newValue: (item: any) => boolean): void;
    protected onSortingFunctionChanged(oldValue: (item: any, otherItem: any) => number, newValue: (item: any, otherItem: any) => number): void;
    _removeContainer(cell: ExtendedListViewCell): void;
    private synchReorderMode();
    private isSwipeEnabled();
    private synchSelection();
    protected onItemReorderChanged(oldValue: boolean, newValue: boolean): void;
    private synchCellReorder();
    private clearCellsAndUpdateHeaderFooter();
    protected onItemSwipeChanged(oldValue: boolean, newValue: boolean): void;
    protected onSwipeActionsChanged(oldValue: boolean, newValue: boolean): void;
    private synchCellSwipe();
    protected onPullToRefreshChanged(oldValue: boolean, newValue: boolean): void;
    private synchPullToRefresh();
    protected onPullToRefreshStyleChanged(oldValue: commonModule.PullToRefreshStyle, newValue: commonModule.PullToRefreshStyle): void;
    protected onLoadOnDemandModeChanged(oldValue: commonModule.ListViewLoadOnDemandMode, newValue: commonModule.ListViewLoadOnDemandMode): void;
    private setLoadOnDemandModeInternal(value);
    private synchLoadOnDemandMode();
    protected onLoadOnDemandBufferSizeChanged(oldValue: number, newValue: number): void;
    private synchLoadOnDemandBufferSize();
    protected onSelectionBehaviorChanged(oldValue: string, newValue: string): void;
    private synchSelectionBehavior();
    private getDataItem(index);
    _getDataItemFromSection(index: number, section: number, isGroup?: boolean): any;
    prepareItem(item: viewModule.View, index: number, section?: number): void;
    prepareItemFromSection(item: viewModule.View, index: number, section: number): void;
    requestLayout(): void;
    private _currentWidthSpec;
    private _currentHeightSpec;
    onMeasure(widthMeasureSpec: number, heightMeasureSpec: number): void;
    readonly _childrenCount: number;
    eachChildView(callback: (child: viewModule.View) => boolean): void;
    onLoaded(): void;
    onUnloaded(): void;
    scrollWithAmount(amount: number, animate: boolean): void;
    getScrollOffset(): number;
    private resolveNativeSnapPosition(snapMode);
    scrollToIndex(index: number, animate?: boolean, snapMode?: string): void;
    notifyPullToRefreshFinished(enableLoadOnDemand?: boolean): void;
    notifyLoadOnDemandFinished(disableLoadOnDemand?: boolean): void;
    _disableLoadOnDemand(): void;
    _returnLoadOnDemandMode(): void;
    notifySwipeToExecuteFinished(): void;
    refresh(): void;
    protected onSourceCollectionChanged(data: any): void;
    private hasFixedItemSize();
    private unbindUnusedCells(removedDataItems);
    private getLoadOnDemandItemTemplateContent();
    _getItemTemplateType(indexPath: NSIndexPath): string;
    private getItemTemplateContent(index, templateType?);
    layoutHeaderFooterCell(cell: any): {
        measuredWidth: number;
        measuredHeight: number;
    };
    layoutLoadOnDemandCell(cell: ExtendedLoadOnDemandCell): {
        measuredWidth: number;
        measuredHeight: number;
    };
    layoutCell(cell: ExtendedListViewCell, indexPath: any): {
        measuredWidth: number;
        measuredHeight: number;
    };
    measureCell(cellView: viewModule.View, sizeRestriction?: any): {
        measuredWidth: number;
        measuredHeight: number;
    };
    private prepareCellTag(cell);
    prepareLoadOnDemandCell(cell: ExtendedLoadOnDemandCell, indexPath: NSIndexPath): void;
    prepareHeaderCell(headerCell: TKListViewHeaderCell, indexPath: NSIndexPath): void;
    prepareFooterCell(footerCell: TKListViewFooterCell, indexPath: NSIndexPath): void;
    private prepareHeaderFooterCell(cell, viewType, indexPath);
    private updateHeaderFooterBindingContext(cell, indexPath);
    private getBindingContext(indexPath);
    prepareCell(tableCell: ExtendedListViewCell, indexPath: NSIndexPath, templateType: string, raiseItemLoadingEvent: boolean): void;
}
