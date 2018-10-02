declare class TKCollectionViewCell extends UICollectionViewCell {

	static alloc(): TKCollectionViewCell; // inherited from NSObject

	static appearance(): TKCollectionViewCell; // inherited from UIAppearance

	static appearanceForTraitCollection(trait: UITraitCollection): TKCollectionViewCell; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedIn(trait: UITraitCollection, ContainerClass: typeof NSObject): TKCollectionViewCell; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedInInstancesOfClasses(trait: UITraitCollection, containerTypes: NSArray<typeof NSObject>): TKCollectionViewCell; // inherited from UIAppearance

	static appearanceWhenContainedIn(ContainerClass: typeof NSObject): TKCollectionViewCell; // inherited from UIAppearance

	static appearanceWhenContainedInInstancesOfClasses(containerTypes: NSArray<typeof NSObject>): TKCollectionViewCell; // inherited from UIAppearance

	static new(): TKCollectionViewCell; // inherited from NSObject

	readonly label: UILabel;
}

declare class TKDataSource extends NSObject implements NSURLConnectionDataDelegate, NSURLConnectionDelegate, UICollectionViewDataSource, UICollectionViewDelegate, UITableViewDataSource, UITableViewDelegate {

	static alloc(): TKDataSource; // inherited from NSObject

	static new(): TKDataSource; // inherited from NSObject

	allowItemsReorder: boolean;

	currentItem: any;

	displayKey: string;

	readonly filterDescriptors: NSArray<TKDataSourceFilterDescriptor>;

	formatter: NSFormatter;

	readonly groupDescriptors: NSArray<TKDataSourceGroupDescriptor>;

	groupItemSourceKey: string;

	itemSource: any;

	readonly items: NSArray<any>;

	mapClass: typeof NSObject;

	mapCollectionsRecursively: boolean;

	propertyMap: NSDictionary<any, any>;

	readonly settings: TKDataSourceSettings;

	readonly sortDescriptors: NSArray<TKDataSourceSortDescriptor>;

	valueKey: string;

	readonly debugDescription: string; // inherited from NSObjectProtocol

	readonly description: string; // inherited from NSObjectProtocol

	readonly hash: number; // inherited from NSObjectProtocol

	readonly isProxy: boolean; // inherited from NSObjectProtocol

	readonly superclass: typeof NSObject; // inherited from NSObjectProtocol

	readonly  // inherited from NSObjectProtocol

	constructor(o: { array: NSArray<any>; });

	constructor(o: { array: NSArray<any>; displayKey: string; });

	constructor(o: { array: NSArray<any>; displayKey: string; valueKey: string; });

	constructor(o: { dataFromJSONResource: string; ofType: string; rootItemKeyPath: string; });

	constructor(o: { dataFromURL: string; dataFormat: TKDataSourceDataFormat; rootItemKeyPath: string; completion: (p1: NSError) => void; });

	constructor(o: { itemSource: any; });

	constructor(o: { JSONString: string; });

	addFilterDescriptor(filterDescriptor: TKDataSourceFilterDescriptor): void;

	addGroupDescriptor(groupDescriptor: TKDataSourceGroupDescriptor): void;

	addSortDescriptor(sortDescriptor: TKDataSourceSortDescriptor): void;

	class(): typeof NSObject;

	collectionViewCanFocusItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): boolean;

	collectionViewCanMoveItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): boolean;

	collectionViewCanPerformActionForItemAtIndexPathWithSender(collectionView: UICollectionView, action: string, indexPath: NSIndexPath, sender: any): boolean;

	collectionViewCellForItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): UICollectionViewCell;

	collectionViewDidDeselectItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): void;

	collectionViewDidEndDisplayingCellForItemAtIndexPath(collectionView: UICollectionView, cell: UICollectionViewCell, indexPath: NSIndexPath): void;

	collectionViewDidEndDisplayingSupplementaryViewForElementOfKindAtIndexPath(collectionView: UICollectionView, view: UICollectionReusableView, elementKind: string, indexPath: NSIndexPath): void;

	collectionViewDidHighlightItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): void;

	collectionViewDidSelectItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): void;

	collectionViewDidUnhighlightItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): void;

	collectionViewDidUpdateFocusInContextWithAnimationCoordinator(collectionView: UICollectionView, context: UICollectionViewFocusUpdateContext, coordinator: UIFocusAnimationCoordinator): void;

	collectionViewIndexPathForIndexTitleAtIndex(collectionView: UICollectionView, title: string, index: number): NSIndexPath;

	collectionViewMoveItemAtIndexPathToIndexPath(collectionView: UICollectionView, sourceIndexPath: NSIndexPath, destinationIndexPath: NSIndexPath): void;

	collectionViewNumberOfItemsInSection(collectionView: UICollectionView, section: number): number;

	collectionViewPerformActionForItemAtIndexPathWithSender(collectionView: UICollectionView, action: string, indexPath: NSIndexPath, sender: any): void;

	collectionViewShouldDeselectItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): boolean;

	collectionViewShouldHighlightItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): boolean;

	collectionViewShouldSelectItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): boolean;

	collectionViewShouldShowMenuForItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): boolean;

	collectionViewShouldSpringLoadItemAtIndexPathWithContext(collectionView: UICollectionView, indexPath: NSIndexPath, context: UISpringLoadedInteractionContext): boolean;

	collectionViewShouldUpdateFocusInContext(collectionView: UICollectionView, context: UICollectionViewFocusUpdateContext): boolean;

	collectionViewTargetContentOffsetForProposedContentOffset(collectionView: UICollectionView, proposedContentOffset: CGPoint): CGPoint;

	collectionViewTargetIndexPathForMoveFromItemAtIndexPathToProposedIndexPath(collectionView: UICollectionView, originalIndexPath: NSIndexPath, proposedIndexPath: NSIndexPath): NSIndexPath;

	collectionViewTransitionLayoutForOldLayoutNewLayout(collectionView: UICollectionView, fromLayout: UICollectionViewLayout, toLayout: UICollectionViewLayout): UICollectionViewTransitionLayout;

	collectionViewViewForSupplementaryElementOfKindAtIndexPath(collectionView: UICollectionView, kind: string, indexPath: NSIndexPath): UICollectionReusableView;

	collectionViewWillDisplayCellForItemAtIndexPath(collectionView: UICollectionView, cell: UICollectionViewCell, indexPath: NSIndexPath): void;

	collectionViewWillDisplaySupplementaryViewForElementKindAtIndexPath(collectionView: UICollectionView, view: UICollectionReusableView, elementKind: string, indexPath: NSIndexPath): void;

	conformsToProtocol(aProtocol: any /* Protocol */): boolean;

	connectionCanAuthenticateAgainstProtectionSpace(connection: NSURLConnection, protectionSpace: NSURLProtectionSpace): boolean;

	connectionDidCancelAuthenticationChallenge(connection: NSURLConnection, challenge: NSURLAuthenticationChallenge): void;

	connectionDidFailWithError(connection: NSURLConnection, error: NSError): void;

	connectionDidFinishLoading(connection: NSURLConnection): void;

	connectionDidReceiveAuthenticationChallenge(connection: NSURLConnection, challenge: NSURLAuthenticationChallenge): void;

	connectionDidReceiveData(connection: NSURLConnection, data: NSData): void;

	connectionDidReceiveResponse(connection: NSURLConnection, response: NSURLResponse): void;

	connectionDidSendBodyDataTotalBytesWrittenTotalBytesExpectedToWrite(connection: NSURLConnection, bytesWritten: number, totalBytesWritten: number, totalBytesExpectedToWrite: number): void;

	connectionNeedNewBodyStream(connection: NSURLConnection, request: NSURLRequest): NSInputStream;

	connectionShouldUseCredentialStorage(connection: NSURLConnection): boolean;

	connectionWillCacheResponse(connection: NSURLConnection, cachedResponse: NSCachedURLResponse): NSCachedURLResponse;

	connectionWillSendRequestForAuthenticationChallenge(connection: NSURLConnection, challenge: NSURLAuthenticationChallenge): void;

	connectionWillSendRequestRedirectResponse(connection: NSURLConnection, request: NSURLRequest, response: NSURLResponse): NSURLRequest;

	enumerate(enumeratorBlock: (p1: any) => void): void;

	filter(filterBlock: (p1: any) => boolean): void;

	filterWithQuery(filterQuery: string): void;

	formatText(formatTextBlock: (p1: any, p2: TKDataSourceGroup) => string): void;

	group(keyForItem: (p1: any) => any): void;

	groupComparator(keyForItem: (p1: any) => any, comparatorBlock: (p1: any, p2: any) => NSComparisonResult): void;

	groupWithKey(propertyName: string): void;

	groupWithKeyComparator(propertyName: string, comparatorBlock: (p1: any, p2: any) => NSComparisonResult): void;

	indexPathForPreferredFocusedViewInCollectionView(collectionView: UICollectionView): NSIndexPath;

	indexPathForPreferredFocusedViewInTableView(tableView: UITableView): NSIndexPath;

	indexTitlesForCollectionView(collectionView: UICollectionView): NSArray<string>;

	initWithArray(items: NSArray<any>): this;

	initWithArrayDisplayKey(items: NSArray<any>, displayKey: string): this;

	initWithArrayDisplayKeyValueKey(items: NSArray<any>, displayKey: string, valueKey: string): this;

	initWithDataFromJSONResourceOfTypeRootItemKeyPath(name: string, type: string, rootItemKeyPath: string): this;

	initWithDataFromURLDataFormatRootItemKeyPathCompletion(url: string, dataFormat: TKDataSourceDataFormat, rootItemKeyPath: string, completion: (p1: NSError) => void): this;

	initWithItemSource(itemSource: any): this;

	initWithJSONString(str: string): this;

	isEqual(object: any): boolean;

	isKindOfClass(aClass: typeof NSObject): boolean;

	isMemberOfClass(aClass: typeof NSObject): boolean;

	loadDataFromJSONResourceOfTypeRootItemKeyPath(name: string, type: string, rootItemKeyPath: string): void;

	loadDataFromJSONStringRootItemKeyPath(string: string, rootItemKeyPath: string): void;

	loadDataFromURLDataFormatRootItemKeyPathCompletion(url: string, dataFormat: TKDataSourceDataFormat, rootItemKeyPath: string, completion: (p1: NSError) => void): void;

	map(mapBlock: (p1: any) => any): void;

	moveItemAtIndexToIndex(fromIndex: number, toIndex: number): void;

	numberOfSectionsInCollectionView(collectionView: UICollectionView): number;

	numberOfSectionsInTableView(tableView: UITableView): number;

	performSelector(aSelector: string): any;

	performSelectorWithObject(aSelector: string, object: any): any;

	performSelectorWithObjectWithObject(aSelector: string, object1: any, object2: any): any;

	reduceWith(initialValue: any, reduceBlock: (p1: any, p2: any) => any): any;

	reloadData(): void;

	removeAllFilterDescriptors(): void;

	removeAllGroupDescriptors(): void;

	removeAllSortDescriptors(): void;

	removeFilterDescriptor(filterDescriptor: TKDataSourceFilterDescriptor): void;

	removeGroupDescriptor(groupDescriptor: TKDataSourceGroupDescriptor): void;

	removeSortDescriptor(sortDescriptor: TKDataSourceSortDescriptor): void;

	respondsToSelector(aSelector: string): boolean;

	retainCount(): number;

	scrollViewDidChangeAdjustedContentInset(scrollView: UIScrollView): void;

	scrollViewDidEndDecelerating(scrollView: UIScrollView): void;

	scrollViewDidEndDraggingWillDecelerate(scrollView: UIScrollView, decelerate: boolean): void;

	scrollViewDidEndScrollingAnimation(scrollView: UIScrollView): void;

	scrollViewDidEndZoomingWithViewAtScale(scrollView: UIScrollView, view: UIView, scale: number): void;

	scrollViewDidScroll(scrollView: UIScrollView): void;

	scrollViewDidScrollToTop(scrollView: UIScrollView): void;

	scrollViewDidZoom(scrollView: UIScrollView): void;

	scrollViewShouldScrollToTop(scrollView: UIScrollView): boolean;

	scrollViewWillBeginDecelerating(scrollView: UIScrollView): void;

	scrollViewWillBeginDragging(scrollView: UIScrollView): void;

	scrollViewWillBeginZoomingWithView(scrollView: UIScrollView, view: UIView): void;

	scrollViewWillEndDraggingWithVelocityTargetContentOffset(scrollView: UIScrollView, velocity: CGPoint, targetContentOffset: interop.Pointer | interop.Reference<CGPoint>): void;

	sectionIndexTitlesForTableView(tableView: UITableView): NSArray<string>;

	self(): this;

	sort(comparatorBlock: (p1: any, p2: any) => NSComparisonResult): void;

	sortWithKeyAscending(propertyName: string, ascending: boolean): void;

	tableViewAccessoryButtonTappedForRowWithIndexPath(tableView: UITableView, indexPath: NSIndexPath): void;

	tableViewAccessoryTypeForRowWithIndexPath(tableView: UITableView, indexPath: NSIndexPath): UITableViewCellAccessoryType;

	tableViewCanEditRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): boolean;

	tableViewCanFocusRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): boolean;

	tableViewCanMoveRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): boolean;

	tableViewCanPerformActionForRowAtIndexPathWithSender(tableView: UITableView, action: string, indexPath: NSIndexPath, sender: any): boolean;

	tableViewCellForRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): UITableViewCell;

	tableViewCommitEditingStyleForRowAtIndexPath(tableView: UITableView, editingStyle: UITableViewCellEditingStyle, indexPath: NSIndexPath): void;

	tableViewDidDeselectRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): void;

	tableViewDidEndDisplayingCellForRowAtIndexPath(tableView: UITableView, cell: UITableViewCell, indexPath: NSIndexPath): void;

	tableViewDidEndDisplayingFooterViewForSection(tableView: UITableView, view: UIView, section: number): void;

	tableViewDidEndDisplayingHeaderViewForSection(tableView: UITableView, view: UIView, section: number): void;

	tableViewDidEndEditingRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): void;

	tableViewDidHighlightRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): void;

	tableViewDidSelectRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): void;

	tableViewDidUnhighlightRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): void;

	tableViewDidUpdateFocusInContextWithAnimationCoordinator(tableView: UITableView, context: UITableViewFocusUpdateContext, coordinator: UIFocusAnimationCoordinator): void;

	tableViewEditActionsForRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): NSArray<UITableViewRowAction>;

	tableViewEditingStyleForRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): UITableViewCellEditingStyle;

	tableViewEstimatedHeightForFooterInSection(tableView: UITableView, section: number): number;

	tableViewEstimatedHeightForHeaderInSection(tableView: UITableView, section: number): number;

	tableViewEstimatedHeightForRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): number;

	tableViewHeightForFooterInSection(tableView: UITableView, section: number): number;

	tableViewHeightForHeaderInSection(tableView: UITableView, section: number): number;

	tableViewHeightForRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): number;

	tableViewIndentationLevelForRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): number;

	tableViewLeadingSwipeActionsConfigurationForRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): UISwipeActionsConfiguration;

	tableViewMoveRowAtIndexPathToIndexPath(tableView: UITableView, sourceIndexPath: NSIndexPath, destinationIndexPath: NSIndexPath): void;

	tableViewNumberOfRowsInSection(tableView: UITableView, section: number): number;

	tableViewPerformActionForRowAtIndexPathWithSender(tableView: UITableView, action: string, indexPath: NSIndexPath, sender: any): void;

	tableViewSectionForSectionIndexTitleAtIndex(tableView: UITableView, title: string, index: number): number;

	tableViewShouldHighlightRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): boolean;

	tableViewShouldIndentWhileEditingRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): boolean;

	tableViewShouldShowMenuForRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): boolean;

	tableViewShouldSpringLoadRowAtIndexPathWithContext(tableView: UITableView, indexPath: NSIndexPath, context: UISpringLoadedInteractionContext): boolean;

	tableViewShouldUpdateFocusInContext(tableView: UITableView, context: UITableViewFocusUpdateContext): boolean;

	tableViewTargetIndexPathForMoveFromRowAtIndexPathToProposedIndexPath(tableView: UITableView, sourceIndexPath: NSIndexPath, proposedDestinationIndexPath: NSIndexPath): NSIndexPath;

	tableViewTitleForDeleteConfirmationButtonForRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): string;

	tableViewTitleForFooterInSection(tableView: UITableView, section: number): string;

	tableViewTitleForHeaderInSection(tableView: UITableView, section: number): string;

	tableViewTrailingSwipeActionsConfigurationForRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): UISwipeActionsConfiguration;

	tableViewViewForFooterInSection(tableView: UITableView, section: number): UIView;

	tableViewViewForHeaderInSection(tableView: UITableView, section: number): UIView;

	tableViewWillBeginEditingRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): void;

	tableViewWillDeselectRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): NSIndexPath;

	tableViewWillDisplayCellForRowAtIndexPath(tableView: UITableView, cell: UITableViewCell, indexPath: NSIndexPath): void;

	tableViewWillDisplayFooterViewForSection(tableView: UITableView, view: UIView, section: number): void;

	tableViewWillDisplayHeaderViewForSection(tableView: UITableView, view: UIView, section: number): void;

	tableViewWillSelectRowAtIndexPath(tableView: UITableView, indexPath: NSIndexPath): NSIndexPath;

	textFromItemInGroup(item: any, group: TKDataSourceGroup): string;

	valueForItemInGroup(item: any, group: TKDataSourceGroup): any;

	viewForZoomingInScrollView(scrollView: UIScrollView): UIView;
}

declare class TKDataSourceCollectionViewSettings extends NSObject {

	static alloc(): TKDataSourceCollectionViewSettings; // inherited from NSObject

	static new(): TKDataSourceCollectionViewSettings; // inherited from NSObject

	createCell(cellIdForItem: (p1: UICollectionView, p2: NSIndexPath, p3: any) => UICollectionViewCell): void;

	initCell(initCellWithItem: (p1: UICollectionView, p2: NSIndexPath, p3: UICollectionViewCell, p4: any) => void): void;
}

declare const enum TKDataSourceDataFormat {

	JSON = 0
}

declare class TKDataSourceFilterDescriptor extends NSObject {

	static alloc(): TKDataSourceFilterDescriptor; // inherited from NSObject

	static new(): TKDataSourceFilterDescriptor; // inherited from NSObject

	readonly filterBlock: (p1: any) => boolean;

	readonly query: string;

	constructor(o: { block: (p1: any) => boolean; });

	constructor(o: { query: string; });

	evaluate(item: any): boolean;

	initWithBlock(filterBlock: (p1: any) => boolean): this;

	initWithQuery(query: string): this;
}

declare class TKDataSourceGroup extends NSObject {

	static alloc(): TKDataSourceGroup; // inherited from NSObject

	static new(): TKDataSourceGroup; // inherited from NSObject

	displayKey: string;

	items: NSArray<any>;

	key: any;

	valueKey: string;

	constructor(o: { items: NSArray<any>; });

	constructor(o: { items: NSArray<any>; valueKey: string; });

	constructor(o: { items: NSArray<any>; valueKey: string; displayKey: string; });

	initWithItems(items: NSArray<any>): this;

	initWithItemsValueKey(items: NSArray<any>, valueKey: string): this;

	initWithItemsValueKeyDisplayKey(items: NSArray<any>, valueKey: string, displayKey: string): this;
}

declare class TKDataSourceGroupDescriptor extends NSObject {

	static alloc(): TKDataSourceGroupDescriptor; // inherited from NSObject

	static new(): TKDataSourceGroupDescriptor; // inherited from NSObject

	readonly comparatorBlock: (p1: any, p2: any) => NSComparisonResult;

	readonly keyForItemBlock: (p1: any) => any;

	propertyName: string;

	constructor(o: { block: (p1: any) => any; });

	constructor(o: { block: (p1: any) => any; comparator: (p1: any, p2: any) => NSComparisonResult; });

	constructor(o: { property: string; });

	constructor(o: { property: string; comparator: (p1: any, p2: any) => NSComparisonResult; });

	initWithBlock(keyForItemBlock: (p1: any) => any): this;

	initWithBlockComparator(keyForItemBlock: (p1: any) => any, comparatorBlock: (p1: any, p2: any) => NSComparisonResult): this;

	initWithProperty(propertyName: string): this;

	initWithPropertyComparator(propertyName: string, comparatorBlock: (p1: any, p2: any) => NSComparisonResult): this;

	keyForItem(item: any): any;
}

declare class TKDataSourceSettings extends NSObject {

	static alloc(): TKDataSourceSettings; // inherited from NSObject

	static new(): TKDataSourceSettings; // inherited from NSObject

	readonly collectionView: TKDataSourceCollectionViewSettings;

	readonly tableView: TKDataSourceTableViewSettings;
}

declare class TKDataSourceSortDescriptor extends NSObject {

	static alloc(): TKDataSourceSortDescriptor; // inherited from NSObject

	static new(): TKDataSourceSortDescriptor; // inherited from NSObject

	ascending: boolean;

	readonly comparator: (p1: any, p2: any) => NSComparisonResult;

	readonly descriptor: NSSortDescriptor;

	propertyName: string;

	constructor(o: { comparator: (p1: any, p2: any) => NSComparisonResult; });

	constructor(o: { property: string; ascending: boolean; });

	initWithComparator(comparator: (p1: any, p2: any) => NSComparisonResult): this;

	initWithPropertyAscending(propertyName: string, ascending: boolean): this;
}

declare class TKDataSourceTableViewSettings extends NSObject {

	static alloc(): TKDataSourceTableViewSettings; // inherited from NSObject

	static new(): TKDataSourceTableViewSettings; // inherited from NSObject

	createCell(createCellForItem: (p1: UITableView, p2: NSIndexPath, p3: any) => UITableViewCell): void;

	initCell(initCellWithItem: (p1: UITableView, p2: NSIndexPath, p3: UITableViewCell, p4: any) => void): void;
}

declare class TKCollectionView extends UICollectionView {

	static alloc(): TKCollectionView; // inherited from NSObject

	static appearance(): TKCollectionView; // inherited from UIAppearance

	static appearanceForTraitCollection(trait: UITraitCollection): TKCollectionView; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedIn(trait: UITraitCollection, ContainerClass: typeof NSObject): TKCollectionView; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedInInstancesOfClasses(trait: UITraitCollection, containerTypes: NSArray<typeof NSObject>): TKCollectionView; // inherited from UIAppearance

	static appearanceWhenContainedIn(ContainerClass: typeof NSObject): TKCollectionView; // inherited from UIAppearance

	static appearanceWhenContainedInInstancesOfClasses(containerTypes: NSArray<typeof NSObject>): TKCollectionView; // inherited from UIAppearance

	static new(): TKCollectionView; // inherited from NSObject

	ownerListView: TKListView;

	skipTouch: boolean;
}

declare class TKListView extends UIView implements UICollectionViewDataSource, UICollectionViewDelegate {

	static alloc(): TKListView; // inherited from NSObject

	static appearance(): TKListView; // inherited from UIAppearance

	static appearanceForTraitCollection(trait: UITraitCollection): TKListView; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedIn(trait: UITraitCollection, ContainerClass: typeof NSObject): TKListView; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedInInstancesOfClasses(trait: UITraitCollection, containerTypes: NSArray<typeof NSObject>): TKListView; // inherited from UIAppearance

	static appearanceWhenContainedIn(ContainerClass: typeof NSObject): TKListView; // inherited from UIAppearance

	static appearanceWhenContainedInInstancesOfClasses(containerTypes: NSArray<typeof NSObject>): TKListView; // inherited from UIAppearance

	static new(): TKListView; // inherited from NSObject

	allowsCellReorder: boolean;

	allowsCellSwipe: boolean;

	allowsMultipleSelection: boolean;

	allowsPullToRefresh: boolean;

	autoRestrictSwipeDirection: boolean;

	autoScrollTreshold: number;

	backgroundView: UIView;

	cellSwipeAnimationDuration: number;

	cellSwipeLimits: UIEdgeInsets;

	cellSwipeTreshold: number;

	collectionView: TKCollectionView;

	contentInset: UIEdgeInsets;

	contentOffset: CGPoint;

	dataSource: TKListViewDataSource;

	delegate: TKListViewDelegate;

	deselectOnSecondTap: boolean;

	readonly indexPathsForSelectedItems: NSArray<any>;

	readonly indexPathsForVisibleItems: NSArray<NSIndexPath>;

	layout: UICollectionViewLayout;

	loadOnDemandBufferSize: number;

	loadOnDemandMode: TKListViewLoadOnDemandMode;

	loadOnDemandView: TKListViewLoadOnDemandView;

	readonly numberOfSections: number;

	pullToRefreshTreshold: number;

	pullToRefreshView: TKListViewPullToRefreshView;

	reorderMode: TKListViewReorderMode;

	scrollDirection: TKListViewScrollDirection;

	selectionBehavior: TKListViewSelectionBehavior;

	readonly visibleCells: NSArray<TKListViewCell>;

	readonly debugDescription: string; // inherited from NSObjectProtocol

	readonly description: string; // inherited from NSObjectProtocol

	readonly hash: number; // inherited from NSObjectProtocol

	readonly isProxy: boolean; // inherited from NSObjectProtocol

	readonly superclass: typeof NSObject; // inherited from NSObjectProtocol

	readonly  // inherited from NSObjectProtocol

	cellForItemAtIndexPath(indexPath: NSIndexPath): TKListViewCell;

	class(): typeof NSObject;

	clearSelectedItems(): void;

	collectionViewCanFocusItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): boolean;

	collectionViewCanMoveItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): boolean;

	collectionViewCanPerformActionForItemAtIndexPathWithSender(collectionView: UICollectionView, action: string, indexPath: NSIndexPath, sender: any): boolean;

	collectionViewCellForItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): UICollectionViewCell;

	collectionViewDidDeselectItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): void;

	collectionViewDidEndDisplayingCellForItemAtIndexPath(collectionView: UICollectionView, cell: UICollectionViewCell, indexPath: NSIndexPath): void;

	collectionViewDidEndDisplayingSupplementaryViewForElementOfKindAtIndexPath(collectionView: UICollectionView, view: UICollectionReusableView, elementKind: string, indexPath: NSIndexPath): void;

	collectionViewDidHighlightItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): void;

	collectionViewDidSelectItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): void;

	collectionViewDidUnhighlightItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): void;

	collectionViewDidUpdateFocusInContextWithAnimationCoordinator(collectionView: UICollectionView, context: UICollectionViewFocusUpdateContext, coordinator: UIFocusAnimationCoordinator): void;

	collectionViewIndexPathForIndexTitleAtIndex(collectionView: UICollectionView, title: string, index: number): NSIndexPath;

	collectionViewMoveItemAtIndexPathToIndexPath(collectionView: UICollectionView, sourceIndexPath: NSIndexPath, destinationIndexPath: NSIndexPath): void;

	collectionViewNumberOfItemsInSection(collectionView: UICollectionView, section: number): number;

	collectionViewPerformActionForItemAtIndexPathWithSender(collectionView: UICollectionView, action: string, indexPath: NSIndexPath, sender: any): void;

	collectionViewShouldDeselectItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): boolean;

	collectionViewShouldHighlightItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): boolean;

	collectionViewShouldSelectItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): boolean;

	collectionViewShouldShowMenuForItemAtIndexPath(collectionView: UICollectionView, indexPath: NSIndexPath): boolean;

	collectionViewShouldSpringLoadItemAtIndexPathWithContext(collectionView: UICollectionView, indexPath: NSIndexPath, context: UISpringLoadedInteractionContext): boolean;

	collectionViewShouldUpdateFocusInContext(collectionView: UICollectionView, context: UICollectionViewFocusUpdateContext): boolean;

	collectionViewTargetContentOffsetForProposedContentOffset(collectionView: UICollectionView, proposedContentOffset: CGPoint): CGPoint;

	collectionViewTargetIndexPathForMoveFromItemAtIndexPathToProposedIndexPath(collectionView: UICollectionView, originalIndexPath: NSIndexPath, proposedIndexPath: NSIndexPath): NSIndexPath;

	collectionViewTransitionLayoutForOldLayoutNewLayout(collectionView: UICollectionView, fromLayout: UICollectionViewLayout, toLayout: UICollectionViewLayout): UICollectionViewTransitionLayout;

	collectionViewViewForSupplementaryElementOfKindAtIndexPath(collectionView: UICollectionView, kind: string, indexPath: NSIndexPath): UICollectionReusableView;

	collectionViewWillDisplayCellForItemAtIndexPath(collectionView: UICollectionView, cell: UICollectionViewCell, indexPath: NSIndexPath): void;

	collectionViewWillDisplaySupplementaryViewForElementKindAtIndexPath(collectionView: UICollectionView, view: UICollectionReusableView, elementKind: string, indexPath: NSIndexPath): void;

	conformsToProtocol(aProtocol: any /* Protocol */): boolean;

	deleteItemsAtIndexPaths(indexPaths: NSArray<any>): void;

	dequeueLoadOnDemandCellForIndexPath(indexPath: NSIndexPath): TKListViewCell;

	dequeueReusableCellWithReuseIdentifierForIndexPath(identifier: string, indexPath: NSIndexPath): any;

	dequeueReusableSupplementaryViewOfKindWithReuseIdentifierForIndexPath(elementKind: string, identifier: string, indexPath: NSIndexPath): any;

	deselectItemAtIndexPathAnimated(indexPath: NSIndexPath, animated: boolean): void;

	didLoadDataOnDemand(): void;

	didRefreshOnPull(): void;

	endSwipe(animated: boolean): void;

	indexPathForCell(cell: UICollectionViewCell): NSIndexPath;

	indexPathForItemAtPoint(point: CGPoint): NSIndexPath;

	indexPathForPreferredFocusedViewInCollectionView(collectionView: UICollectionView): NSIndexPath;

	indexTitlesForCollectionView(collectionView: UICollectionView): NSArray<string>;

	insertItemsAtIndexPaths(indexPaths: NSArray<any>): void;

	isEqual(object: any): boolean;

	isKindOfClass(aClass: typeof NSObject): boolean;

	isMemberOfClass(aClass: typeof NSObject): boolean;

	moveItemAtIndexPathToIndexPath(indexPath: NSIndexPath, newIndexPath: NSIndexPath): void;

	numberOfItemsInSection(section: number): number;

	numberOfSectionsInCollectionView(collectionView: UICollectionView): number;

	performBatchUpdatesCompletion(updates: () => void, completion: (p1: boolean) => void): void;

	performSelector(aSelector: string): any;

	performSelectorWithObject(aSelector: string, object: any): any;

	performSelectorWithObjectWithObject(aSelector: string, object1: any, object2: any): any;

	registerClassForCellWithReuseIdentifier(cellClass: typeof NSObject, identifier: string): void;

	registerClassForSupplementaryViewOfKindWithReuseIdentifier(viewClass: typeof NSObject, elementKind: string, identifier: string): void;

	registerLoadOnDemandCell(cellClass: typeof NSObject): void;

	registerNibForCellReuseIdentifier(nib: UINib, identifier: string): void;

	registerNibForSupplementaryViewOfKindWithReuseIdentifier(nib: UINib, elementKind: string, identifier: string): void;

	reloadData(): void;

	reloadItemsAtIndexPaths(indexPaths: NSArray<any>): void;

	respondsToSelector(aSelector: string): boolean;

	retainCount(): number;

	scrollToItemAtIndexPathAtScrollPositionAnimated(indexPath: NSIndexPath, scrollPosition: UICollectionViewScrollPosition, animated: boolean): void;

	scrollViewDidChangeAdjustedContentInset(scrollView: UIScrollView): void;

	scrollViewDidEndDecelerating(scrollView: UIScrollView): void;

	scrollViewDidEndDraggingWillDecelerate(scrollView: UIScrollView, decelerate: boolean): void;

	scrollViewDidEndScrollingAnimation(scrollView: UIScrollView): void;

	scrollViewDidEndZoomingWithViewAtScale(scrollView: UIScrollView, view: UIView, scale: number): void;

	scrollViewDidScroll(scrollView: UIScrollView): void;

	scrollViewDidScrollToTop(scrollView: UIScrollView): void;

	scrollViewDidZoom(scrollView: UIScrollView): void;

	scrollViewShouldScrollToTop(scrollView: UIScrollView): boolean;

	scrollViewWillBeginDecelerating(scrollView: UIScrollView): void;

	scrollViewWillBeginDragging(scrollView: UIScrollView): void;

	scrollViewWillBeginZoomingWithView(scrollView: UIScrollView, view: UIView): void;

	scrollViewWillEndDraggingWithVelocityTargetContentOffset(scrollView: UIScrollView, velocity: CGPoint, targetContentOffset: interop.Pointer | interop.Reference<CGPoint>): void;

	selectItemAtIndexPathAnimatedScrollPosition(indexPath: NSIndexPath, animated: boolean, scrollPosition: UICollectionViewScrollPosition): void;

	self(): this;

	setContentOffsetAnimated(contentOffset: CGPoint, animated: boolean): void;

	viewForZoomingInScrollView(scrollView: UIScrollView): UIView;
}

declare class TKListViewCell extends TKListViewReusableCell {

	static alloc(): TKListViewCell; // inherited from NSObject

	static appearance(): TKListViewCell; // inherited from UIAppearance

	static appearanceForTraitCollection(trait: UITraitCollection): TKListViewCell; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedIn(trait: UITraitCollection, ContainerClass: typeof NSObject): TKListViewCell; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedInInstancesOfClasses(trait: UITraitCollection, containerTypes: NSArray<typeof NSObject>): TKListViewCell; // inherited from UIAppearance

	static appearanceWhenContainedIn(ContainerClass: typeof NSObject): TKListViewCell; // inherited from UIAppearance

	static appearanceWhenContainedInInstancesOfClasses(containerTypes: NSArray<typeof NSObject>): TKListViewCell; // inherited from UIAppearance

	static new(): TKListViewCell; // inherited from NSObject

	contentInsets: UIEdgeInsets;

	readonly detailTextLabel: UILabel;

	readonly imageView: UIImageView;

	offsetContentViewInMultipleSelection: boolean;

	reorderHandle: UIView;

	readonly swipeBackgroundView: UIView;

	shouldSelect(): boolean;
}

declare class TKListViewCellBackgroundView extends TKView {

	static alloc(): TKListViewCellBackgroundView; // inherited from NSObject

	static appearance(): TKListViewCellBackgroundView; // inherited from UIAppearance

	static appearanceForTraitCollection(trait: UITraitCollection): TKListViewCellBackgroundView; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedIn(trait: UITraitCollection, ContainerClass: typeof NSObject): TKListViewCellBackgroundView; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedInInstancesOfClasses(trait: UITraitCollection, containerTypes: NSArray<typeof NSObject>): TKListViewCellBackgroundView; // inherited from UIAppearance

	static appearanceWhenContainedIn(ContainerClass: typeof NSObject): TKListViewCellBackgroundView; // inherited from UIAppearance

	static appearanceWhenContainedInInstancesOfClasses(containerTypes: NSArray<typeof NSObject>): TKListViewCellBackgroundView; // inherited from UIAppearance

	static new(): TKListViewCellBackgroundView; // inherited from NSObject

	allowsMultipleSelection: boolean;

	checkInset: number;

	readonly checkView: TKCheckView;

	isSelectedBackground: boolean;

	isVertical: boolean;

	updateStyle(): void;
}

interface TKListViewDataSource extends NSObjectProtocol {

	listViewCellForItemAtIndexPathIsInitial(listView: TKListView, indexPath: NSIndexPath, isInitial: boolean): TKListViewCell;

	listViewNumberOfItemsInSection(listView: TKListView, section: number): number;

	listViewViewForSupplementaryElementOfKindAtIndexPath?(listView: TKListView, kind: string, indexPath: NSIndexPath): TKListViewReusableCell;

	numberOfSectionsInListView?(listView: TKListView): number;
}
declare var TKListViewDataSource: {

	prototype: TKListViewDataSource;
};

interface TKListViewDelegate extends UIScrollViewDelegate {

	listViewDidDeselectItemAtIndexPath?(listView: TKListView, indexPath: NSIndexPath): void;

	listViewDidFinishSwipeCellAtIndexPathWithOffset?(listView: TKListView, cell: TKListViewCell, indexPath: NSIndexPath, offset: CGPoint): void;

	listViewDidHighlightItemAtIndexPath?(listView: TKListView, indexPath: NSIndexPath): void;

	listViewDidLongPressCellAtIndexPath?(listView: TKListView, cell: TKListViewCell, indexPath: NSIndexPath): void;

	listViewDidPullWithOffset?(listView: TKListView, offset: number): void;

	listViewDidReorderItemFromIndexPathToIndexPath?(listView: TKListView, originalIndexPath: NSIndexPath, targetIndexPath: NSIndexPath): void;

	listViewDidSelectItemAtIndexPath?(listView: TKListView, indexPath: NSIndexPath): void;

	listViewDidSwipeCellAtIndexPathWithOffset?(listView: TKListView, cell: TKListViewCell, indexPath: NSIndexPath, offset: CGPoint): void;

	listViewDidUnhighlightItemAtIndexPath?(listView: TKListView, indexPath: NSIndexPath): void;

	listViewScrollViewDidEndDecelerating?(listView: TKListView, scrollView: UIScrollView): void;

	listViewScrollViewDidEndDraggingWillDecelerate?(listView: TKListView, scrollView: UIScrollView, decelerate: boolean): void;

	listViewScrollViewDidScroll?(listView: TKListView, scrollView: UIScrollView): void;

	listViewScrollViewWillBeginDragging?(listView: TKListView, scrollView: UIScrollView): void;

	listViewShouldDeselectItemAtIndexPath?(listView: TKListView, indexPath: NSIndexPath): boolean;

	listViewShouldHighlightItemAtIndexPath?(listView: TKListView, indexPath: NSIndexPath): boolean;

	listViewShouldLoadMoreDataAtIndexPath?(listView: TKListView, indexPath: NSIndexPath): boolean;

	listViewShouldRefreshOnPull?(listView: TKListView): boolean;

	listViewShouldSelectItemAtIndexPath?(listView: TKListView, indexPath: NSIndexPath): boolean;

	listViewShouldSwipeCellAtIndexPath?(listView: TKListView, cell: TKListViewCell, indexPath: NSIndexPath): boolean;

	listViewWillReorderItemAtIndexPath?(listView: TKListView, indexPath: NSIndexPath): boolean;
}
declare var TKListViewDelegate: {

	prototype: TKListViewDelegate;
};

declare var TKListViewElementKindSectionFooter: string;

declare var TKListViewElementKindSectionHeader: string;

declare class TKListViewFooterCell extends TKListViewReusableCell {

	static alloc(): TKListViewFooterCell; // inherited from NSObject

	static appearance(): TKListViewFooterCell; // inherited from UIAppearance

	static appearanceForTraitCollection(trait: UITraitCollection): TKListViewFooterCell; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedIn(trait: UITraitCollection, ContainerClass: typeof NSObject): TKListViewFooterCell; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedInInstancesOfClasses(trait: UITraitCollection, containerTypes: NSArray<typeof NSObject>): TKListViewFooterCell; // inherited from UIAppearance

	static appearanceWhenContainedIn(ContainerClass: typeof NSObject): TKListViewFooterCell; // inherited from UIAppearance

	static appearanceWhenContainedInInstancesOfClasses(containerTypes: NSArray<typeof NSObject>): TKListViewFooterCell; // inherited from UIAppearance

	static new(): TKListViewFooterCell; // inherited from NSObject
}

declare class TKListViewGridLayout extends TKListViewLinearLayout {

	static alloc(): TKListViewGridLayout; // inherited from NSObject

	static new(): TKListViewGridLayout; // inherited from NSObject

	lineSpacing: number;

	spanCount: number;
}

declare class TKListViewGroupLayoutChange extends TKListViewLayoutChange {

	static alloc(): TKListViewGroupLayoutChange; // inherited from NSObject

	static new(): TKListViewGroupLayoutChange; // inherited from NSObject

	isHeader: boolean;
}

declare class TKListViewGroupLayoutChangeManager extends TKListViewLayoutChangeManager {

	static alloc(): TKListViewGroupLayoutChangeManager; // inherited from NSObject

	static new(): TKListViewGroupLayoutChangeManager; // inherited from NSObject

	isHeader: boolean;
}

declare class TKListViewHeaderCell extends TKListViewReusableCell {

	static alloc(): TKListViewHeaderCell; // inherited from NSObject

	static appearance(): TKListViewHeaderCell; // inherited from UIAppearance

	static appearanceForTraitCollection(trait: UITraitCollection): TKListViewHeaderCell; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedIn(trait: UITraitCollection, ContainerClass: typeof NSObject): TKListViewHeaderCell; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedInInstancesOfClasses(trait: UITraitCollection, containerTypes: NSArray<typeof NSObject>): TKListViewHeaderCell; // inherited from UIAppearance

	static appearanceWhenContainedIn(ContainerClass: typeof NSObject): TKListViewHeaderCell; // inherited from UIAppearance

	static appearanceWhenContainedInInstancesOfClasses(containerTypes: NSArray<typeof NSObject>): TKListViewHeaderCell; // inherited from UIAppearance

	static new(): TKListViewHeaderCell; // inherited from NSObject
}

declare const enum TKListViewItemAlignment {

	Stretch = 0,

	Left = 1,

	Center = 2,

	Right = 3
}

declare const enum TKListViewItemAnimation {

	Default = 0,

	Fade = 1,

	Scale = 2,

	Slide = 3
}

declare class TKListViewLayoutChange extends NSObject {

	static alloc(): TKListViewLayoutChange; // inherited from NSObject

	static new(): TKListViewLayoutChange; // inherited from NSObject

	delta: number;

	from: NSIndexPath;

	to: NSIndexPath;

	constructor(o: { indexPath: NSIndexPath; andDelta: number; });

	apply(attributes: UICollectionViewLayoutAttributes): boolean;

	applyToAll(layout: UICollectionViewLayout): void;

	compareWith(first: NSIndexPath, second: NSIndexPath): NSComparisonResult;

	endsWith(attributes: UICollectionViewLayoutAttributes): boolean;

	initWithIndexPathAndDelta(indexPath: NSIndexPath, delta: number): this;

	intersectsWith(change: TKListViewLayoutChange): boolean;

	isAfter(attributes: UICollectionViewLayoutAttributes): boolean;

	isValid(): boolean;

	itemIsBeforeEndIn(attributes: UICollectionViewLayoutAttributes, layout: TKListViewLayoutChangeManager): boolean;

	power(): number;

	shouldApply(indexPath: NSIndexPath): boolean;

	startIsBefore(object: TKListViewLayoutChange): boolean;

	startsWith(attributes: UICollectionViewLayoutAttributes): boolean;
}

declare class TKListViewLayoutChangeManager extends NSObject {

	static alloc(): TKListViewLayoutChangeManager; // inherited from NSObject

	static new(): TKListViewLayoutChangeManager; // inherited from NSObject

	changes: NSMutableArray<any>;

	layout: UICollectionViewLayout;

	constructor(o: { layout: UICollectionViewLayout; });

	addChange(change: TKListViewLayoutChange): void;

	applyChange(attributes: UICollectionViewLayoutAttributes): void;

	decreaseIndexPath(indexPath: NSIndexPath): NSIndexPath;

	increaseIndexPath(indexPath: NSIndexPath): NSIndexPath;

	initWithLayout(layout: UICollectionViewLayout): this;

	optimize(): void;
}

declare class TKListViewLinearLayout extends UICollectionViewLayout {

	static alloc(): TKListViewLinearLayout; // inherited from NSObject

	static new(): TKListViewLinearLayout; // inherited from NSObject

	animationDuration: number;

	delegate: TKListViewLinearLayoutDelegate;

	dynamicItemSize: boolean;

	footerReferenceSize: CGSize;

	headerReferenceSize: CGSize;

	itemAlignment: TKListViewItemAlignment;

	itemAppearAnimation: TKListViewItemAnimation;

	itemDeleteAnimation: TKListViewItemAnimation;

	itemInsertAnimation: TKListViewItemAnimation;

	itemSize: CGSize;

	itemSpacing: number;

	owner: TKListView;

	scrollDirection: TKListViewScrollDirection;

	calculatedItemWidth(): number;

	initFooterAttributesAtPoint(attributes: UICollectionViewLayoutAttributes, point: CGPoint): CGPoint;

	initHeaderAttributesAtPoint(attributes: UICollectionViewLayoutAttributes, point: CGPoint): CGPoint;

	initItemAttributesAtPointLastInSection(attributes: UICollectionViewLayoutAttributes, point: CGPoint, lastInSection: boolean): CGPoint;

	layoutSectionAtPoint(section: number, location: CGPoint): CGPoint;
}

interface TKListViewLinearLayoutDelegate extends NSObjectProtocol {

	listViewLayoutSizeForItemAtIndexPath(listView: TKListView, layout: TKListViewLinearLayout, indexPath: NSIndexPath): CGSize;
}
declare var TKListViewLinearLayoutDelegate: {

	prototype: TKListViewLinearLayoutDelegate;
};

declare class TKListViewLoadOnDemandCell extends TKListViewCell {

	static alloc(): TKListViewLoadOnDemandCell; // inherited from NSObject

	static appearance(): TKListViewLoadOnDemandCell; // inherited from UIAppearance

	static appearanceForTraitCollection(trait: UITraitCollection): TKListViewLoadOnDemandCell; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedIn(trait: UITraitCollection, ContainerClass: typeof NSObject): TKListViewLoadOnDemandCell; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedInInstancesOfClasses(trait: UITraitCollection, containerTypes: NSArray<typeof NSObject>): TKListViewLoadOnDemandCell; // inherited from UIAppearance

	static appearanceWhenContainedIn(ContainerClass: typeof NSObject): TKListViewLoadOnDemandCell; // inherited from UIAppearance

	static appearanceWhenContainedInInstancesOfClasses(containerTypes: NSArray<typeof NSObject>): TKListViewLoadOnDemandCell; // inherited from UIAppearance

	static new(): TKListViewLoadOnDemandCell; // inherited from NSObject

	activityIndicator: UIActivityIndicatorView;

	updateState(): void;
}

declare const enum TKListViewLoadOnDemandMode {

	None = 0,

	Manual = 1,

	Auto = 2
}

declare class TKListViewLoadOnDemandView extends UIView {

	static alloc(): TKListViewLoadOnDemandView; // inherited from NSObject

	static appearance(): TKListViewLoadOnDemandView; // inherited from UIAppearance

	static appearanceForTraitCollection(trait: UITraitCollection): TKListViewLoadOnDemandView; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedIn(trait: UITraitCollection, ContainerClass: typeof NSObject): TKListViewLoadOnDemandView; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedInInstancesOfClasses(trait: UITraitCollection, containerTypes: NSArray<typeof NSObject>): TKListViewLoadOnDemandView; // inherited from UIAppearance

	static appearanceWhenContainedIn(ContainerClass: typeof NSObject): TKListViewLoadOnDemandView; // inherited from UIAppearance

	static appearanceWhenContainedInInstancesOfClasses(containerTypes: NSArray<typeof NSObject>): TKListViewLoadOnDemandView; // inherited from UIAppearance

	static new(): TKListViewLoadOnDemandView; // inherited from NSObject
}

declare class TKListViewPullToRefreshView extends UIView {

	static alloc(): TKListViewPullToRefreshView; // inherited from NSObject

	static appearance(): TKListViewPullToRefreshView; // inherited from UIAppearance

	static appearanceForTraitCollection(trait: UITraitCollection): TKListViewPullToRefreshView; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedIn(trait: UITraitCollection, ContainerClass: typeof NSObject): TKListViewPullToRefreshView; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedInInstancesOfClasses(trait: UITraitCollection, containerTypes: NSArray<typeof NSObject>): TKListViewPullToRefreshView; // inherited from UIAppearance

	static appearanceWhenContainedIn(ContainerClass: typeof NSObject): TKListViewPullToRefreshView; // inherited from UIAppearance

	static appearanceWhenContainedInInstancesOfClasses(containerTypes: NSArray<typeof NSObject>): TKListViewPullToRefreshView; // inherited from UIAppearance

	static new(): TKListViewPullToRefreshView; // inherited from NSObject

	readonly activityIndicator: UIActivityIndicatorView;

	startAnimating(): void;

	stopAnimating(): void;
}

declare class TKListViewReorderHandle extends UIView {

	static alloc(): TKListViewReorderHandle; // inherited from NSObject

	static appearance(): TKListViewReorderHandle; // inherited from UIAppearance

	static appearanceForTraitCollection(trait: UITraitCollection): TKListViewReorderHandle; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedIn(trait: UITraitCollection, ContainerClass: typeof NSObject): TKListViewReorderHandle; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedInInstancesOfClasses(trait: UITraitCollection, containerTypes: NSArray<typeof NSObject>): TKListViewReorderHandle; // inherited from UIAppearance

	static appearanceWhenContainedIn(ContainerClass: typeof NSObject): TKListViewReorderHandle; // inherited from UIAppearance

	static appearanceWhenContainedInInstancesOfClasses(containerTypes: NSArray<typeof NSObject>): TKListViewReorderHandle; // inherited from UIAppearance

	static new(): TKListViewReorderHandle; // inherited from NSObject

	lineInsets: UIEdgeInsets;

	lineStroke: TKStroke;

	rowCount: number;

	rowSpacing: number;
}

declare const enum TKListViewReorderMode {

	WithHandle = 0,

	WithLongPress = 1
}

declare class TKListViewReusableCell extends UICollectionViewCell {

	static alloc(): TKListViewReusableCell; // inherited from NSObject

	static appearance(): TKListViewReusableCell; // inherited from UIAppearance

	static appearanceForTraitCollection(trait: UITraitCollection): TKListViewReusableCell; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedIn(trait: UITraitCollection, ContainerClass: typeof NSObject): TKListViewReusableCell; // inherited from UIAppearance

	static appearanceForTraitCollectionWhenContainedInInstancesOfClasses(trait: UITraitCollection, containerTypes: NSArray<typeof NSObject>): TKListViewReusableCell; // inherited from UIAppearance

	static appearanceWhenContainedIn(ContainerClass: typeof NSObject): TKListViewReusableCell; // inherited from UIAppearance

	static appearanceWhenContainedInInstancesOfClasses(containerTypes: NSArray<typeof NSObject>): TKListViewReusableCell; // inherited from UIAppearance

	static new(): TKListViewReusableCell; // inherited from NSObject

	readonly textLabel: UILabel;
}

declare const enum TKListViewScrollDirection {

	Vertical = 0,

	Horizontal = 1
}

declare const enum TKListViewSelectionBehavior {

	None = 0,

	Press = 1,

	LongPress = 2
}

declare class TKListViewStaggeredLayout extends TKListViewGridLayout {

	static alloc(): TKListViewStaggeredLayout; // inherited from NSObject

	static new(): TKListViewStaggeredLayout; // inherited from NSObject

	alignLastLine: boolean;
}

declare class TKListViewStaggeredLayoutInfo extends NSObject {

	static alloc(): TKListViewStaggeredLayoutInfo; // inherited from NSObject

	static new(): TKListViewStaggeredLayoutInfo; // inherited from NSObject

	attributes: UICollectionViewLayoutAttributes;

	frame: CGRect;

	itemSize: CGSize;

	constructor(o: { frame: CGRect; andIndexPath: UICollectionViewLayoutAttributes; itemSize: CGSize; });

	initWithFrameAndIndexPathItemSize(frame: CGRect, attributes: UICollectionViewLayoutAttributes, itemSize: CGSize): this;
}

declare var TNSListViewVersionNumber: number;

declare var TNSListViewVersionString: interop.Reference<number>;
