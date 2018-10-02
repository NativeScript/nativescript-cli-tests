declare module com {
	export module telerik {
		export module android {
			export module data {
				export class AndroidDataSourceAdapter<E>  extends com.telerik.android.data.DataSourceAdapterBase<any> {
					public static class: java.lang.Class<com.telerik.android.data.AndroidDataSourceAdapter<any>>;
					public selectionChanged(param0: com.telerik.android.data.SelectionChangeInfo<any>): void;
					public areAllItemsEnabled(): boolean;
					public selectionChanged(param0: com.telerik.android.data.SelectionChangeInfo<com.telerik.android.data.DataItem<any>>): void;
					public onNothingSelected(param0: globalAndroid.widget.AdapterView<any>): void;
					public getDropDownView(param0: number, param1: globalAndroid.view.View, param2: globalAndroid.view.ViewGroup): globalAndroid.view.View;
					public onItemSelected(param0: globalAndroid.widget.AdapterView<any>, param1: globalAndroid.view.View, param2: number, param3: number): void;
					public constructor();
					public constructor(param0: java.util.List<any>, param1: globalAndroid.content.Context, param2: globalAndroid.widget.AdapterView<any>);
					public onItemClick(param0: globalAndroid.widget.AdapterView<any>, param1: globalAndroid.view.View, param2: number, param3: number): void;
					public constructor(param0: java.util.List<any>, param1: globalAndroid.content.Context);
					public isEnabled(param0: number): boolean;
					public currentItemChanged(param0: com.telerik.android.data.CurrentItemChangedInfo<any>): void;
					public dataChanged(param0: com.telerik.android.data.DataChangeInfo<any>): void;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module android {
			export module data {
				export class CurrencyService<E>  extends java.lang.Object {
					public static class: java.lang.Class<com.telerik.android.data.CurrencyService<any>>;
					public constructor(param0: java.util.List<E>);
					public movePrevious(): boolean;
					public addCurrentChangedListener(param0: com.telerik.android.data.CurrentItemChangedListener<E>): void;
					public onCurrentItemChanged(param0: E, param1: E): void;
					public getCurrentItem(): E;
					public setCurrentItem(param0: E): void;
					public removeCurrentChangedListener(param0: com.telerik.android.data.CurrentItemChangedListener<E>): boolean;
					public isCurrent(param0: E): boolean;
					public moveFirst(): void;
					public moveNext(): boolean;
					public moveLast(): void;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module android {
			export module data {
				export class CurrentItemChangedInfo<E>  extends java.lang.Object {
					public static class: java.lang.Class<com.telerik.android.data.CurrentItemChangedInfo<any>>;
					public constructor(param0: E, param1: E);
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module android {
			export module data {
				export class CurrentItemChangedListener<E>  extends java.lang.Object {
					public static class: java.lang.Class<com.telerik.android.data.CurrentItemChangedListener<any>>;
					/**
					 * Constructs a new instance of the com.telerik.android.data.CurrentItemChangedListener<any> interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
					 */
					public constructor(implementation: {
						currentItemChanged(param0: com.telerik.android.data.CurrentItemChangedInfo<E>): void;
					});
					public constructor();
					public currentItemChanged(param0: com.telerik.android.data.CurrentItemChangedInfo<E>): void;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module android {
			export module data {
				export class DataChangeInfo<E>  extends java.lang.Object {
					public static class: java.lang.Class<com.telerik.android.data.DataChangeInfo<any>>;
					public constructor();
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module android {
			export module data {
				export class DataChangedListener<E>  extends java.lang.Object {
					public static class: java.lang.Class<com.telerik.android.data.DataChangedListener<any>>;
					/**
					 * Constructs a new instance of the com.telerik.android.data.DataChangedListener<any> interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
					 */
					public constructor(implementation: {
						dataChanged(param0: com.telerik.android.data.DataChangeInfo<E>): void;
					});
					public constructor();
					public dataChanged(param0: com.telerik.android.data.DataChangeInfo<E>): void;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module android {
			export module data {
				export class DataItem<E>  extends java.lang.Object {
					public static class: java.lang.Class<com.telerik.android.data.DataItem<any>>;
					public toString(): string;
					public entity(): E;
					public setListItems(param0: java.util.List<com.telerik.android.data.DataItem<E>>): void;
					public constructor(param0: E, param1: any);
					public constructor(param0: E);
					public getItems(): java.util.List<com.telerik.android.data.DataItem<E>>;
					public groupKey(): any;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module android {
			export module data {
				export class DataSourceAdapterBase<E>  extends globalAndroid.widget.BaseAdapter {
					public static class: java.lang.Class<com.telerik.android.data.DataSourceAdapterBase<any>>;
					public selectionChanged(param0: com.telerik.android.data.SelectionChangeInfo<any>): void;
					public getCount(): number;
					public selectionChanged(param0: com.telerik.android.data.SelectionChangeInfo<com.telerik.android.data.DataItem<any>>): void;
					public areAllItemsEnabled(): boolean;
					public dataSource(): com.telerik.android.data.RadDataSource<any>;
					public getDropDownView(param0: number, param1: globalAndroid.view.View, param2: globalAndroid.view.ViewGroup): globalAndroid.view.View;
					public createCurrentView(param0: com.telerik.android.data.DataItem<any>): globalAndroid.view.View;
					public getView(param0: number, param1: globalAndroid.view.View, param2: globalAndroid.view.ViewGroup): globalAndroid.view.View;
					public selectionService(): com.telerik.android.data.SelectionService<com.telerik.android.data.DataItem<any>>;
					public getItem(param0: number): any;
					public constructor();
					public constructor(param0: java.util.List<any>, param1: globalAndroid.content.Context);
					public currentItemChanged(param0: com.telerik.android.data.CurrentItemChangedInfo<any>): void;
					public isEnabled(param0: number): boolean;
					public getViewType(): com.telerik.android.data.DataSourceAdapterBase.ViewType;
					public getItemId(param0: number): number;
					public dataChanged(param0: com.telerik.android.data.DataChangeInfo<any>): void;
					public setViewType(param0: com.telerik.android.data.DataSourceAdapterBase.ViewType): void;
				}
				export module DataSourceAdapterBase {
					export class ViewType {
						public static class: java.lang.Class<com.telerik.android.data.DataSourceAdapterBase.ViewType>;
						public static FLAT: com.telerik.android.data.DataSourceAdapterBase.ViewType;
						public static HIERARCHY: com.telerik.android.data.DataSourceAdapterBase.ViewType;
						public static valueOf(param0: java.lang.Class<any>, param1: string): java.lang.Enum<any>;
						public static values(): native.Array<com.telerik.android.data.DataSourceAdapterBase.ViewType>;
						public static valueOf(param0: string): com.telerik.android.data.DataSourceAdapterBase.ViewType;
					}
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module android {
			export module data {
				export class LoadJSONTask extends globalAndroid.os.AsyncTask<any,any,any> {
					public static class: java.lang.Class<com.telerik.android.data.LoadJSONTask>;
					public setFinishedListener(param0: com.telerik.android.common.Procedure<any>): void;
					public constructor();
					public doInBackground(param0: native.Array<any>): any;
					public onPostExecute(param0: any): void;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module android {
			export module data {
				export class OnJSONDataSourceCreated extends java.lang.Object {
					public static class: java.lang.Class<com.telerik.android.data.OnJSONDataSourceCreated>;
					/**
					 * Constructs a new instance of the com.telerik.android.data.OnJSONDataSourceCreated interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
					 */
					public constructor(implementation: {
						onError(param0: org.json.JSONException): void;
						onDataSourceCreated(param0: com.telerik.android.data.RadDataSource<org.json.JSONObject>): void;
					});
					public constructor();
					public onError(param0: org.json.JSONException): void;
					public onDataSourceCreated(param0: com.telerik.android.data.RadDataSource<org.json.JSONObject>): void;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module android {
			export module data {
				export class RadDataSource<E>  extends java.lang.Object {
					public static class: java.lang.Class<com.telerik.android.data.RadDataSource<any>>;
					public suspendUpdate(): void;
					public collectionChanged(param0: com.telerik.android.common.CollectionChangedEvent<E>): void;
					public groupDescriptors(): com.telerik.android.common.ObservableCollection<com.telerik.android.common.Function<E,any>>;
					public resumeUpdate(): void;
					public removeDataChangeListener(param0: com.telerik.android.data.DataChangedListener<E>): void;
					public view(): java.util.List<com.telerik.android.data.DataItem<E>>;
					public addDataChangeListener(param0: com.telerik.android.data.DataChangedListener<E>): void;
					public setSource(param0: java.lang.Iterable<E>): void;
					public iterator(): java.util.Iterator<com.telerik.android.data.DataItem<E>>;
					public filterDescriptors(): com.telerik.android.common.ObservableCollection<com.telerik.android.common.Function<E,java.lang.Boolean>>;
					public invalidateDescriptors(): void;
					public sortDescriptors(): com.telerik.android.common.ObservableCollection<com.telerik.android.common.Function2<E,E,java.lang.Integer>>;
					public iterator(): java.util.Iterator<any>;
					public static createFromJsonUrl(param0: java.net.URL, param1: com.telerik.android.data.OnJSONDataSourceCreated): void;
					public getSource(): java.lang.Iterable<E>;
					public constructor();
					public constructor(param0: java.lang.Iterable<E>);
					public onDataChanged(): void;
					public static createFromJson(param0: string): com.telerik.android.data.RadDataSource<org.json.JSONObject>;
					public resumeUpdate(param0: boolean): void;
					public flatView(): java.util.List<com.telerik.android.data.DataItem<E>>;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module android {
			export module data {
				export class RadDataSourceAdapter<E>  extends com.telerik.android.data.DataSourceAdapterBase<any> {
					public static class: java.lang.Class<com.telerik.android.data.RadDataSourceAdapter<any>>;
					public selectionChanged(param0: com.telerik.android.data.SelectionChangeInfo<any>): void;
					public areAllItemsEnabled(): boolean;
					public selectionChanged(param0: com.telerik.android.data.SelectionChangeInfo<com.telerik.android.data.DataItem<any>>): void;
					public constructor();
					public constructor(param0: java.util.List<any>, param1: globalAndroid.content.Context);
					public getDropDownView(param0: number, param1: globalAndroid.view.View, param2: globalAndroid.view.ViewGroup): globalAndroid.view.View;
					public isEnabled(param0: number): boolean;
					public currentItemChanged(param0: com.telerik.android.data.CurrentItemChangedInfo<any>): void;
					public dataChanged(param0: com.telerik.android.data.DataChangeInfo<any>): void;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module android {
			export module data {
				export class SelectionAdapter extends java.lang.Object {
					public static class: java.lang.Class<com.telerik.android.data.SelectionAdapter>;
					/**
					 * Constructs a new instance of the com.telerik.android.data.SelectionAdapter interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
					 */
					public constructor(implementation: {
						clearSelection(): void;
						isIndexSelected(param0: number): boolean;
						deselectIndex(param0: number): void;
						selectIndex(param0: number): void;
						selectedItemsSize(): number;
						setSelectionMode(param0: com.telerik.android.data.SelectionMode): void;
						getSelectionMode(): com.telerik.android.data.SelectionMode;
						getSelectedItems(): java.util.List<any>;
						getSelectedIndices(): native.Array<number>;
					});
					public constructor();
					public getSelectedIndices(): native.Array<number>;
					public getSelectionMode(): com.telerik.android.data.SelectionMode;
					public selectIndex(param0: number): void;
					public deselectIndex(param0: number): void;
					public selectedItemsSize(): number;
					public clearSelection(): void;
					public isIndexSelected(param0: number): boolean;
					public setSelectionMode(param0: com.telerik.android.data.SelectionMode): void;
					public getSelectedItems(): java.util.List<any>;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module android {
			export module data {
				export class SelectionChangeInfo<E>  extends java.lang.Object {
					public static class: java.lang.Class<com.telerik.android.data.SelectionChangeInfo<any>>;
					public selectedItems(): java.lang.Iterable<E>;
					public constructor(param0: java.util.List<E>, param1: java.util.List<E>);
					public deselectedItems(): java.lang.Iterable<E>;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module android {
			export module data {
				export class SelectionChangeListener<E>  extends java.lang.Object {
					public static class: java.lang.Class<com.telerik.android.data.SelectionChangeListener<any>>;
					/**
					 * Constructs a new instance of the com.telerik.android.data.SelectionChangeListener<any> interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
					 */
					public constructor(implementation: {
						selectionChanged(param0: com.telerik.android.data.SelectionChangeInfo<E>): void;
					});
					public constructor();
					public selectionChanged(param0: com.telerik.android.data.SelectionChangeInfo<E>): void;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module android {
			export module data {
				export class SelectionMode {
					public static class: java.lang.Class<com.telerik.android.data.SelectionMode>;
					public static NONE: com.telerik.android.data.SelectionMode;
					public static SINGLE: com.telerik.android.data.SelectionMode;
					public static MULTIPLE: com.telerik.android.data.SelectionMode;
					public static valueOf(param0: string): com.telerik.android.data.SelectionMode;
					public static values(): native.Array<com.telerik.android.data.SelectionMode>;
					public static valueOf(param0: java.lang.Class<any>, param1: string): java.lang.Enum<any>;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module android {
			export module data {
				export class SelectionService<E>  extends java.lang.Object {
					public static class: java.lang.Class<com.telerik.android.data.SelectionService<any>>;
					public get(param0: number): E;
					public removeSelectionChangeListener(param0: com.telerik.android.data.SelectionChangeListener<E>): boolean;
					public setSelectionMode(param0: com.telerik.android.data.SelectionMode): void;
					public clearSelection(): void;
					public onSelectionChanged(param0: java.util.List<E>, param1: java.util.List<E>): void;
					public getSelectionMode(): com.telerik.android.data.SelectionMode;
					public constructor();
					public selectedItemsSize(): number;
					public selectItems(param0: java.util.List<E>): void;
					public addSelectionChangeListener(param0: com.telerik.android.data.SelectionChangeListener<E>): void;
					public selectItem(param0: E): void;
					public deselectItem(param0: E): void;
					public isItemSelected(param0: E): boolean;
					public selectedItems(): java.util.List<E>;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class BuildConfig extends java.lang.Object {
					public static class: java.lang.Class<com.telerik.widget.list.BuildConfig>;
					public static DEBUG: boolean;
					public static APPLICATION_ID: string;
					public static BUILD_TYPE: string;
					public static FLAVOR: string;
					public static VERSION_CODE: number;
					public static VERSION_NAME: string;
					public constructor();
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class CollapsedGroupState extends java.lang.Object {
					public static class: java.lang.Class<com.telerik.widget.list.CollapsedGroupState>;
					/**
					 * Constructs a new instance of the com.telerik.widget.list.CollapsedGroupState interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
					 */
					public constructor(implementation: {
						getCollapsedGroupPositions(): native.Array<number>;
						clearCollapsedGroups(): void;
						isGroupCollapsed(param0: number): boolean;
						isGroupCollapsed(param0: any): boolean;
						collapseGroupAtPosition(param0: number): void;
						expandGroupAtPosition(param0: number): void;
						setOwner(param0: com.telerik.widget.list.RadListView): void;
						addListener(param0: com.telerik.widget.list.CollapsibleGroupsBehavior.CollapseGroupListener): void;
						removeListener(param0: com.telerik.widget.list.CollapsibleGroupsBehavior.CollapseGroupListener): void;
					});
					public constructor();
					public isGroupCollapsed(param0: number): boolean;
					public expandGroupAtPosition(param0: number): void;
					public isGroupCollapsed(param0: any): boolean;
					public addListener(param0: com.telerik.widget.list.CollapsibleGroupsBehavior.CollapseGroupListener): void;
					public collapseGroupAtPosition(param0: number): void;
					public removeListener(param0: com.telerik.widget.list.CollapsibleGroupsBehavior.CollapseGroupListener): void;
					public clearCollapsedGroups(): void;
					public getCollapsedGroupPositions(): native.Array<number>;
					public setOwner(param0: com.telerik.widget.list.RadListView): void;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class CollapsedViewHolder extends com.telerik.widget.list.ListViewHolder {
					public static class: java.lang.Class<com.telerik.widget.list.CollapsedViewHolder>;
					public constructor(param0: globalAndroid.view.View);
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class CollapsibleGroupsBehavior extends com.telerik.widget.list.ListViewBehavior {
					public static class: java.lang.Class<com.telerik.widget.list.CollapsibleGroupsBehavior>;
					public constructor(param0: number, param1: com.telerik.widget.list.CollapsedGroupState);
					public onSaveInstanceState(param0: globalAndroid.os.Parcelable): void;
					public onDetached(param0: com.telerik.widget.list.RadListView): void;
					public getExpandImageResource(): number;
					public isGroupCollapsed(param0: any): boolean;
					public addListener(param0: com.telerik.widget.list.CollapsibleGroupsBehavior.CollapseGroupListener): void;
					public setCollapseImageResource(param0: number): void;
					public getCollapseImageResource(): number;
					public setExpandImageResource(param0: number): void;
					public onTapUp(param0: globalAndroid.view.MotionEvent): boolean;
					public constructor();
					public onRestoreInstanceState(param0: globalAndroid.os.Parcelable): void;
					public expandAll(): void;
					public removeListener(param0: com.telerik.widget.list.CollapsibleGroupsBehavior.CollapseGroupListener): void;
					public onAttached(param0: com.telerik.widget.list.RadListView): void;
					public collapseAll(): void;
					public constructor(param0: number);
					public changeIsGroupCollapsed(param0: any): void;
				}
				export module CollapsibleGroupsBehavior {
					export class CollapseGroupListener extends java.lang.Object {
						public static class: java.lang.Class<com.telerik.widget.list.CollapsibleGroupsBehavior.CollapseGroupListener>;
						/**
						 * Constructs a new instance of the com.telerik.widget.list.CollapsibleGroupsBehavior$CollapseGroupListener interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
						 */
						public constructor(implementation: {
							onGroupCollapsed(param0: any): void;
							onGroupExpanded(param0: any): void;
						});
						public constructor();
						public onGroupExpanded(param0: any): void;
						public onGroupCollapsed(param0: any): void;
					}
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class CurrentPositionChangeListener extends java.lang.Object {
					public static class: java.lang.Class<com.telerik.widget.list.CurrentPositionChangeListener>;
					/**
					 * Constructs a new instance of the com.telerik.widget.list.CurrentPositionChangeListener interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
					 */
					public constructor(implementation: {
						onCurrentPositionChanged(param0: number, param1: number): void;
					});
					public constructor();
					public onCurrentPositionChanged(param0: number, param1: number): void;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class DeckOfCardsLayoutManager extends com.telerik.widget.list.SlideLayoutManagerBase {
					public static class: java.lang.Class<com.telerik.widget.list.DeckOfCardsLayoutManager>;
					public static HORIZONTAL: number;
					public static VERTICAL: number;
					public setPerspectiveItemsCount(param0: number): void;
					public scaleXForIndex(param0: number): number;
					public alphaForIndex(param0: number): number;
					public isAutoDissolveFrontView(): boolean;
					public elevationForIndex(param0: number): number;
					public layoutView(param0: globalAndroid.view.View): void;
					public canScroll(param0: number): boolean;
					public nextIndex(param0: number): number;
					public computeHorizontalScrollExtent(param0: globalAndroid.support.v7.widget.RecyclerView.State): number;
					public scaleYForIndex(param0: number): number;
					public calculateFrontViewSize(): void;
					public computeHorizontalScrollOffset(param0: globalAndroid.support.v7.widget.RecyclerView.State): number;
					public computeScrollVectorForPosition(param0: number): globalAndroid.graphics.PointF;
					public fill(param0: number, param1: globalAndroid.support.v7.widget.RecyclerView.Recycler, param2: globalAndroid.support.v7.widget.RecyclerView.State): void;
					public setAutoDissolveFrontView(param0: boolean): void;
					public constructor();
					public calculateScrollProgress(): number;
					public translationXForIndex(param0: number): number;
					public translationYForIndex(param0: number): number;
					public computeVerticalScrollExtent(param0: globalAndroid.support.v7.widget.RecyclerView.State): number;
					public generateDefaultLayoutParams(): globalAndroid.support.v7.widget.RecyclerView.LayoutParams;
					public getDirection(param0: number): number;
					public constructor(param0: globalAndroid.content.Context, param1: number, param2: boolean);
					public computeVerticalScrollRange(param0: globalAndroid.support.v7.widget.RecyclerView.State): number;
					public previousItemsCount(): number;
					public computeVerticalScrollOffset(param0: globalAndroid.support.v7.widget.RecyclerView.State): number;
					public handleItemRemoved(param0: number, param1: globalAndroid.support.v7.widget.RecyclerView.Recycler, param2: globalAndroid.support.v7.widget.RecyclerView.State): void;
					public computeHorizontalScrollRange(param0: globalAndroid.support.v7.widget.RecyclerView.State): number;
					public constructor(param0: globalAndroid.content.Context);
					public previousIndex(param0: number): number;
					public animationDuration(): number;
					public layoutIndexForAdapterPosition(param0: number): number;
					public nextItemsCount(): number;
					public onRestoreInstanceState(param0: globalAndroid.os.Parcelable): void;
					public onSaveInstanceState(): globalAndroid.os.Parcelable;
					public perspective(): com.telerik.widget.list.PerspectiveChangeInfo;
					public smoothScrollToPosition(param0: globalAndroid.support.v7.widget.RecyclerView, param1: globalAndroid.support.v7.widget.RecyclerView.State, param2: number): void;
					public getPerspectiveItemsCount(): number;
					public adapterPositionForLayoutIndex(param0: number): number;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class DefaultCollapsedGroupState extends java.lang.Object implements com.telerik.widget.list.CollapsedGroupState {
					public static class: java.lang.Class<com.telerik.widget.list.DefaultCollapsedGroupState>;
					public isGroupCollapsed(param0: number): boolean;
					public expandGroupAtPosition(param0: number): void;
					public addListener(param0: com.telerik.widget.list.CollapsibleGroupsBehavior.CollapseGroupListener): void;
					public isGroupCollapsed(param0: any): boolean;
					public removeListener(param0: com.telerik.widget.list.CollapsibleGroupsBehavior.CollapseGroupListener): void;
					public collapseGroupAtPosition(param0: number): void;
					public clearCollapsedGroups(): void;
					public getCollapsedGroupPositions(): native.Array<number>;
					public setOwner(param0: com.telerik.widget.list.RadListView): void;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class DefaultSelectionAdapter<E>  extends com.telerik.android.data.SelectionAdapter {
					public static class: java.lang.Class<com.telerik.widget.list.DefaultSelectionAdapter<any>>;
					public getSelectedIndices(): native.Array<number>;
					public getSelectionMode(): com.telerik.android.data.SelectionMode;
					public selectIndex(param0: number): void;
					public deselectIndex(param0: number): void;
					public selectedItemsSize(): number;
					public setOwner(param0: com.telerik.widget.list.ListViewAdapter): void;
					public clearSelection(): void;
					public isIndexSelected(param0: number): boolean;
					public setSelectionMode(param0: com.telerik.android.data.SelectionMode): void;
					public constructor(param0: com.telerik.android.data.SelectionService<any>);
					public getSelectedItems(): java.util.List<any>;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class FadeItemAnimator extends com.telerik.widget.list.ListViewItemAnimator {
					public static class: java.lang.Class<com.telerik.widget.list.FadeItemAnimator>;
					public getAlpha(): number;
					public animateViewAddedPrepare(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public onAnimationAddEnded(param0: globalAndroid.support.v4.view.ViewPropertyAnimatorCompat, param1: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public constructor();
					public removeAnimation(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): globalAndroid.support.v4.view.ViewPropertyAnimatorCompat;
					public onAnimationRemoveEnded(param0: globalAndroid.support.v4.view.ViewPropertyAnimatorCompat, param1: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public setAlpha(param0: number): void;
					public addAnimation(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): globalAndroid.support.v4.view.ViewPropertyAnimatorCompat;
					public onAnimationAddCancelled(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class GroupAdapter extends java.lang.Object {
					public static class: java.lang.Class<com.telerik.widget.list.GroupAdapter>;
					/**
					 * Constructs a new instance of the com.telerik.widget.list.GroupAdapter interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
					 */
					public constructor(implementation: {
						isGroupHeader(param0: number): boolean;
					});
					public constructor();
					public isGroupHeader(param0: number): boolean;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class ItemAnimatorSet extends com.telerik.widget.list.ListViewItemAnimator {
					public static class: java.lang.Class<com.telerik.widget.list.ItemAnimatorSet>;
					public onDetached(param0: com.telerik.widget.list.RadListView): void;
					public animateViewRemovedImpl(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public animateViewAddedPrepare(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public constructor();
					public endAnimation(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public removeAnimator(param0: com.telerik.widget.list.ListViewItemAnimator): void;
					public clearAnimators(): void;
					public animateViewAddedImpl(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public onAttached(param0: com.telerik.widget.list.RadListView): void;
					public addAnimator(param0: com.telerik.widget.list.ListViewItemAnimator): void;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class ItemReorderBehavior extends com.telerik.widget.list.ListViewBehavior {
					public static class: java.lang.Class<com.telerik.widget.list.ItemReorderBehavior>;
					public endReorder(param0: boolean): void;
					public onDispatchDraw(param0: globalAndroid.graphics.Canvas): void;
					public removeListener(param0: com.telerik.widget.list.ItemReorderBehavior.ItemReorderListener): void;
					public getScrollValue(): number;
					public onLongPress(param0: globalAndroid.view.MotionEvent): void;
					public setScrollValue(param0: number): void;
					public isInProgress(): boolean;
					public startReorder(param0: number, param1: number): void;
					public moveReorderImage(param0: number, param1: number, param2: number, param3: number): void;
					public constructor();
					public onLongPressDragEnded(param0: boolean): boolean;
					public onLongPressDrag(param0: number, param1: number, param2: number, param3: number): void;
					public addListener(param0: com.telerik.widget.list.ItemReorderBehavior.ItemReorderListener): void;
					public onAttached(param0: com.telerik.widget.list.RadListView): void;
					public createReorderImage(param0: globalAndroid.view.View): globalAndroid.graphics.drawable.BitmapDrawable;
					public onFling(param0: globalAndroid.view.MotionEvent, param1: globalAndroid.view.MotionEvent, param2: number, param3: number): boolean;
				}
				export module ItemReorderBehavior {
					export class ItemReorderListener extends java.lang.Object {
						public static class: java.lang.Class<com.telerik.widget.list.ItemReorderBehavior.ItemReorderListener>;
						/**
						 * Constructs a new instance of the com.telerik.widget.list.ItemReorderBehavior$ItemReorderListener interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
						 */
						public constructor(implementation: {
							onReorderStarted(param0: number): void;
							onReorderItem(param0: number, param1: number): void;
							onReorderFinished(): void;
						});
						public constructor();
						public onReorderFinished(): void;
						public onReorderStarted(param0: number): void;
						public onReorderItem(param0: number, param1: number): void;
					}
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class ListViewAdapter extends com.telerik.widget.list.ListViewAdapterBase {
					public static class: java.lang.Class<com.telerik.widget.list.ListViewAdapter>;
					public reorderItem(param0: number, param1: number): boolean;
					public constructor(param0: java.util.List<any>);
					public remove(param0: number): any;
					public getPosition(param0: any): number;
					public getItemId(param0: any): number;
					public onCreateViewHolder(param0: globalAndroid.view.ViewGroup, param1: number): any;
					public getSelectionServiceProvider(): com.telerik.android.data.SelectionAdapter;
					public constructor();
					public constructor(param0: java.util.List<any>, param1: com.telerik.android.data.SelectionAdapter);
					public getItems(): java.util.List<any>;
					public updateSwipeLayoutParams(param0: com.telerik.widget.list.ListViewHolder, param1: boolean): void;
					public remove(param0: any): boolean;
					public add(param0: any): void;
					public add(param0: number, param1: any): void;
					public onCreateViewHolder(param0: globalAndroid.view.ViewGroup, param1: number): com.telerik.widget.list.ListViewHolder;
					public updateMainLayoutParams(param0: com.telerik.widget.list.ListViewHolder, param1: boolean): void;
					public onBindViewHolder(param0: com.telerik.widget.list.ListViewHolder, param1: number): void;
					public getItem(param0: number): any;
					public onBindViewHolder(param0: any, param1: number): void;
					public getPosition(param0: number): number;
					public setItems(param0: java.util.List<any>): void;
					public getItemCount(): number;
					public onBindViewHolder(param0: any, param1: number, param2: java.util.List<any>): void;
					public updateLayoutParams(param0: com.telerik.widget.list.ListViewHolder, param1: boolean): void;
					public getItemId(param0: number): number;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export abstract class ListViewAdapterBase extends globalAndroid.support.v7.widget.RecyclerView.Adapter<com.telerik.widget.list.ListViewHolder> {
					public static class: java.lang.Class<com.telerik.widget.list.ListViewAdapterBase>;
					public static ITEM_VIEW_TYPE_HEADER: number;
					public static ITEM_VIEW_TYPE_FOOTER: number;
					public static ITEM_VIEW_TYPE_TOP_INDICATOR: number;
					public static ITEM_VIEW_TYPE_BOTTOM_INDICATOR: number;
					public static ITEM_VIEW_TYPE_SWIPE_CONTENT: number;
					public static ITEM_VIEW_TYPE_EMPTY_CONTENT: number;
					public static ITEM_VIEW_TYPE_COLLAPSED: number;
					public static INVALID_ID: number;
					public canDeselect(param0: number): boolean;
					public reorderItem(param0: number, param1: number): boolean;
					public notifySwipeExecuteFinished(): void;
					public onCreateViewHolder(param0: globalAndroid.view.ViewGroup, param1: number): com.telerik.widget.list.ListViewHolder;
					public onCreateListViewHolder(param0: globalAndroid.view.ViewGroup, param1: number): com.telerik.widget.list.ListViewHolder;
					public notifyRefreshFinished(): void;
					public onBindViewHolder(param0: com.telerik.widget.list.ListViewHolder, param1: number): void;
					public isGroupHeader(param0: number): boolean;
					public getSelectionServiceProvider(): com.telerik.android.data.SelectionAdapter;
					public onBindViewHolder(param0: any, param1: number): void;
					public onCreateViewHolder(param0: globalAndroid.view.ViewGroup, param1: number): any;
					public constructor();
					public canSelect(param0: number): boolean;
					public onBindListViewHolder(param0: com.telerik.widget.list.ListViewHolder, param1: number): void;
					public onBindViewHolder(param0: any, param1: number, param2: java.util.List<any>): void;
					public onCreateSwipeContentHolder(param0: globalAndroid.view.ViewGroup): com.telerik.widget.list.ListViewHolder;
					public updateLayoutParams(param0: com.telerik.widget.list.ListViewHolder, param1: boolean): void;
					public notifyLoadingFinished(): void;
					public onBindSwipeContentHolder(param0: com.telerik.widget.list.ListViewHolder, param1: number): void;
					public canSwipe(param0: number): boolean;
					public isPositionValid(param0: number): boolean;
					public canReorder(param0: number): boolean;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class ListViewBehavior extends java.lang.Object {
					public static class: java.lang.Class<com.telerik.widget.list.ListViewBehavior>;
					public bindViewHolder(param0: com.telerik.widget.list.ListViewHolder, param1: number): void;
					public onSaveInstanceState(param0: globalAndroid.os.Parcelable): void;
					public onDetached(param0: com.telerik.widget.list.RadListView): void;
					public createViewHolder(param0: globalAndroid.view.ViewGroup, param1: number): com.telerik.widget.list.ListViewHolder;
					public onDispatchDraw(param0: globalAndroid.graphics.Canvas): void;
					public onScrolled(param0: number, param1: number): void;
					public owner(): com.telerik.widget.list.RadListView;
					public onInterceptTouchEvent(param0: globalAndroid.view.MotionEvent): boolean;
					public onLongPress(param0: globalAndroid.view.MotionEvent): void;
					public getItemViewType(param0: number, param1: number): number;
					public isInProgress(): boolean;
					public onTapUp(param0: globalAndroid.view.MotionEvent): boolean;
					public onActionUpOrCancel(param0: boolean): boolean;
					public constructor();
					public onLongPressDragEnded(param0: boolean): boolean;
					public onRestoreInstanceState(param0: globalAndroid.os.Parcelable): void;
					public onLayout(param0: boolean, param1: number, param2: number, param3: number, param4: number): void;
					public onLongPressDrag(param0: number, param1: number, param2: number, param3: number): void;
					public onAttached(param0: com.telerik.widget.list.RadListView): void;
					public managesViewHolders(): boolean;
					public onShortPressDrag(param0: number, param1: number, param2: number, param3: number): boolean;
					public onFling(param0: globalAndroid.view.MotionEvent, param1: globalAndroid.view.MotionEvent, param2: number, param3: number): boolean;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class ListViewDataSourceAdapter extends com.telerik.widget.list.ListViewAdapter implements com.telerik.android.data.DataChangedListener<any> {
					public static class: java.lang.Class<com.telerik.widget.list.ListViewDataSourceAdapter>;
					public static ITEM_VIEW_TYPE_GROUP: number;
					public getGroupViewType(param0: any): number;
					public clearFilterDescriptors(): void;
					public reorderItem(param0: number, param1: number): boolean;
					public constructor(param0: java.util.List<any>);
					public removeFilterDescriptor(param0: com.telerik.android.common.Function<any,java.lang.Boolean>): void;
					public removeGroupDescriptor(param0: com.telerik.android.common.Function<any,any>): void;
					public invalidateDescriptors(): void;
					public getItemViewType(param0: any): number;
					public getPosition(param0: any): number;
					public getItemId(param0: any): number;
					public constructor(param0: com.telerik.android.data.RadDataSource<any>);
					public constructor(param0: java.util.List<any>, param1: com.telerik.android.data.SelectionAdapter);
					public constructor();
					public dataChanged(param0: com.telerik.android.data.DataChangeInfo<any>): void;
					public onCreateItemViewHolder(param0: globalAndroid.view.ViewGroup, param1: number): com.telerik.widget.list.ListViewHolder;
					public add(param0: any): void;
					public add(param0: number, param1: any): void;
					public addFilterDescriptor(param0: com.telerik.android.common.Function<any,java.lang.Boolean>): void;
					public getPosition(param0: number): number;
					public setItems(param0: java.util.List<any>): void;
					public addSortDescriptor(param0: com.telerik.android.common.Function2<any,any,java.lang.Integer>): void;
					public canSwipe(param0: number): boolean;
					public onBindItemViewHolder(param0: com.telerik.widget.list.ListViewHolder, param1: any): void;
					public remove(param0: number, param1: boolean): any;
					public getHeaderPosition(param0: number): number;
					public getDataItem(param0: number): com.telerik.android.data.DataItem<any>;
					public add(param0: number, param1: any, param2: boolean): void;
					public removeSortDescriptor(param0: com.telerik.android.common.Function2<any,any,java.lang.Integer>): void;
					public clearSortDescriptors(): void;
					public remove(param0: number): any;
					public onCreateViewHolder(param0: globalAndroid.view.ViewGroup, param1: number): any;
					public getItemViewType(param0: number): number;
					public dataChanged(param0: com.telerik.android.data.DataChangeInfo<any>): void;
					public addGroupDescriptor(param0: com.telerik.android.common.Function<any,any>): void;
					public canReorder(param0: number): boolean;
					public remove(param0: any): boolean;
					public getBaseItemCount(): number;
					public constructor(param0: java.util.List<any>, param1: com.telerik.android.data.RadDataSource<any>);
					public remove(param0: any, param1: boolean): boolean;
					public onCreateViewHolder(param0: globalAndroid.view.ViewGroup, param1: number): com.telerik.widget.list.ListViewHolder;
					public onCreateGroupViewHolder(param0: globalAndroid.view.ViewGroup, param1: number): com.telerik.widget.list.ListViewHolder;
					public onBindViewHolder(param0: com.telerik.widget.list.ListViewHolder, param1: number): void;
					public getItem(param0: number): any;
					public isGroupHeader(param0: number): boolean;
					public clearGroupDescriptors(): void;
					public onBindViewHolder(param0: any, param1: number): void;
					public add(param0: any, param1: boolean): void;
					public canSelect(param0: number): boolean;
					public getItemCount(): number;
					public onBindViewHolder(param0: any, param1: number, param2: java.util.List<any>): void;
					public getItemId(param0: number): number;
					public onBindGroupViewHolder(param0: com.telerik.widget.list.ListViewHolder, param1: any): void;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class ListViewGestureListener extends globalAndroid.view.GestureDetector.SimpleOnGestureListener {
					public static class: java.lang.Class<com.telerik.widget.list.ListViewGestureListener>;
					public owner: com.telerik.widget.list.RadListView;
					public onDoubleTap(param0: globalAndroid.view.MotionEvent): boolean;
					public onInterceptTouchEvent(param0: com.telerik.widget.list.RadListView, param1: globalAndroid.view.MotionEvent): boolean;
					public onLongPress(param0: globalAndroid.view.MotionEvent): void;
					public onSingleTapUp(param0: globalAndroid.view.MotionEvent): boolean;
					public constructor(param0: globalAndroid.content.Context);
					public onScroll(param0: globalAndroid.view.MotionEvent, param1: globalAndroid.view.MotionEvent, param2: number, param3: number): boolean;
					public onDown(param0: globalAndroid.view.MotionEvent): boolean;
					public onTouchEvent(param0: com.telerik.widget.list.RadListView, param1: globalAndroid.view.MotionEvent): boolean;
					public onTapUp(param0: globalAndroid.view.MotionEvent): boolean;
					public onActionUpOrCancel(param0: boolean): boolean;
					public constructor();
					public onLongPressDragEnded(param0: boolean): boolean;
					public onLongPressDrag(param0: number, param1: number, param2: number, param3: number): void;
					public onSingleTapConfirmed(param0: globalAndroid.view.MotionEvent): boolean;
					public onShowPress(param0: globalAndroid.view.MotionEvent): void;
					public onDoubleTapEvent(param0: globalAndroid.view.MotionEvent): boolean;
					public onShortPressDrag(param0: number, param1: number, param2: number, param3: number): boolean;
					public onFling(param0: globalAndroid.view.MotionEvent, param1: globalAndroid.view.MotionEvent, param2: number, param3: number): boolean;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class ListViewHolder extends globalAndroid.support.v7.widget.RecyclerView.ViewHolder {
					public static class: java.lang.Class<com.telerik.widget.list.ListViewHolder>;
					public constructor(param0: globalAndroid.view.View);
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export abstract class ListViewItemAnimator extends globalAndroid.support.v7.widget.SimpleItemAnimator {
					public static class: java.lang.Class<com.telerik.widget.list.ListViewItemAnimator>;
					public static ADD: number;
					public static REMOVE: number;
					public owner: com.telerik.widget.list.RadListView;
					public mAddAnimations: java.util.ArrayList<globalAndroid.support.v7.widget.RecyclerView.ViewHolder>;
					public mRemoveAnimations: java.util.ArrayList<globalAndroid.support.v7.widget.RecyclerView.ViewHolder>;
					public alreadyAppearedViews: java.util.HashSet<java.lang.Long>;
					public getType(): number;
					public onDetached(param0: com.telerik.widget.list.RadListView): void;
					public animateViewRemovedImpl(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public onAnimationRemoveStarted(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public removeAnimation(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): globalAndroid.support.v4.view.ViewPropertyAnimatorCompat;
					public onEndAnimation(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public onMeasure(): void;
					public animateViewAppeared(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): boolean;
					public animateViewRemoved(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): boolean;
					public animateChange(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder, param1: globalAndroid.support.v7.widget.RecyclerView.ViewHolder, param2: number, param3: number, param4: number, param5: number): boolean;
					public animateViewAdded(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): boolean;
					public constructor();
					public onAnimationAddStarted(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public animateViewAppearedImpl(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public setType(param0: number): void;
					public onAttached(param0: com.telerik.widget.list.RadListView): void;
					public animateChange(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder, param1: globalAndroid.support.v7.widget.RecyclerView.ViewHolder, param2: globalAndroid.support.v7.widget.RecyclerView.ItemAnimator.ItemHolderInfo, param3: globalAndroid.support.v7.widget.RecyclerView.ItemAnimator.ItemHolderInfo): boolean;
					public isRunning(param0: globalAndroid.support.v7.widget.RecyclerView.ItemAnimator.ItemAnimatorFinishedListener): boolean;
					public animateMove(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder, param1: number, param2: number, param3: number, param4: number): boolean;
					public animateViewAddedPrepare(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public onAnimationAddEnded(param0: globalAndroid.support.v4.view.ViewPropertyAnimatorCompat, param1: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public endAnimations(): void;
					public animateRemove(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): boolean;
					public runPendingAnimations(): void;
					public animateViewDisappearedImpl(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public dispatchFinishedWhenDone(): void;
					public addAnimation(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): globalAndroid.support.v4.view.ViewPropertyAnimatorCompat;
					public animateAdd(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): boolean;
					public animateMoveImpl(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder, param1: number, param2: number, param3: number, param4: number): void;
					public onAnimationRemoveCancelled(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public onAnimationRemoveEnded(param0: globalAndroid.support.v4.view.ViewPropertyAnimatorCompat, param1: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public endAnimation(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public animateChangeImpl(param0: com.telerik.widget.list.ListViewItemAnimator.ChangeInfo): void;
					public isRunning(): boolean;
					public animateViewDisappeared(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): boolean;
					public animateViewAddedImpl(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public onAnimationAddCancelled(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
				}
				export module ListViewItemAnimator {
					export class ChangeInfo extends java.lang.Object {
						public static class: java.lang.Class<com.telerik.widget.list.ListViewItemAnimator.ChangeInfo>;
						public oldHolder: globalAndroid.support.v7.widget.RecyclerView.ViewHolder;
						public newHolder: globalAndroid.support.v7.widget.RecyclerView.ViewHolder;
						public fromX: number;
						public fromY: number;
						public toX: number;
						public toY: number;
						public toString(): string;
					}
					export class MoveInfo extends java.lang.Object {
						public static class: java.lang.Class<com.telerik.widget.list.ListViewItemAnimator.MoveInfo>;
						public holder: globalAndroid.support.v7.widget.RecyclerView.ViewHolder;
						public fromX: number;
						public fromY: number;
						public toX: number;
						public toY: number;
						public constructor(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder, param1: number, param2: number, param3: number, param4: number);
					}
					export class VpaListenerAdapter extends java.lang.Object implements globalAndroid.support.v4.view.ViewPropertyAnimatorListener {
						public static class: java.lang.Class<com.telerik.widget.list.ListViewItemAnimator.VpaListenerAdapter>;
						public onAnimationStart(param0: globalAndroid.view.View): void;
						public onAnimationCancel(param0: globalAndroid.view.View): void;
						public constructor();
						public onAnimationEnd(param0: globalAndroid.view.View): void;
					}
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class ListViewTextHolder extends com.telerik.widget.list.ListViewHolder {
					public static class: java.lang.Class<com.telerik.widget.list.ListViewTextHolder>;
					public textView: globalAndroid.widget.TextView;
					public constructor(param0: globalAndroid.view.View, param1: number);
					public constructor(param0: globalAndroid.view.View);
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class ListViewWrapperAdapter extends com.telerik.widget.list.ListViewAdapterBase {
					public static class: java.lang.Class<com.telerik.widget.list.ListViewWrapperAdapter>;
					public addRefreshListener(param0: com.telerik.widget.list.SwipeRefreshBehavior.RefreshListener): void;
					public handleSwipeStart(param0: number, param1: number, param2: number): void;
					public removeRefreshListener(param0: com.telerik.widget.list.SwipeRefreshBehavior.RefreshListener): void;
					public unregisterAdapterDataObserver(param0: globalAndroid.support.v7.widget.RecyclerView.AdapterDataObserver): void;
					public reorderItem(param0: number, param1: number): boolean;
					public onCreateListViewHolder(param0: globalAndroid.view.ViewGroup, param1: number): com.telerik.widget.list.ListViewHolder;
					public registerAdapterDataObserver(param0: globalAndroid.support.v7.widget.RecyclerView.AdapterDataObserver): void;
					public removeLoadingListener(param0: com.telerik.widget.list.LoadOnDemandBehavior.LoadingListener): void;
					public isGroupHeader(param0: number): boolean;
					public removeSwipeExecuteDismissedListener(param0: com.telerik.widget.list.SwipeExecuteBehavior.SwipeExecuteDismissedListener): void;
					public getSelectionServiceProvider(): com.telerik.android.data.SelectionAdapter;
					public getPositionInWrapperAdapter(param0: number): number;
					public addLoadingListener(param0: com.telerik.widget.list.LoadOnDemandBehavior.LoadingListener): void;
					public onBindListViewHolder(param0: com.telerik.widget.list.ListViewHolder, param1: number): void;
					public getItemCount(): number;
					public addSwipeExecuteDismissedListener(param0: com.telerik.widget.list.SwipeExecuteBehavior.SwipeExecuteDismissedListener): void;
					public onCreateSwipeContentHolder(param0: globalAndroid.view.ViewGroup): com.telerik.widget.list.ListViewHolder;
					public getPositionInOriginalAdapter(param0: number): number;
					public getItemViewType(param0: number): number;
					public onBindSwipeContentHolder(param0: com.telerik.widget.list.ListViewHolder, param1: number): void;
					public getItemId(param0: number): number;
				}
				export module ListViewWrapperAdapter {
					export class WrappedDataObserver extends globalAndroid.support.v7.widget.RecyclerView.AdapterDataObserver {
						public static class: java.lang.Class<com.telerik.widget.list.ListViewWrapperAdapter.WrappedDataObserver>;
						public constructor();
						public onChanged(): void;
						public onItemRangeMoved(param0: number, param1: number, param2: number): void;
						public constructor(param0: com.telerik.widget.list.ListViewWrapperAdapter, param1: globalAndroid.support.v7.widget.RecyclerView.AdapterDataObserver);
						public onItemRangeChanged(param0: number, param1: number): void;
						public onItemRangeChanged(param0: number, param1: number, param2: any): void;
						public onItemRangeInserted(param0: number, param1: number): void;
						public onItemRangeRemoved(param0: number, param1: number): void;
					}
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class LoadOnDemandBehavior extends com.telerik.widget.list.ListViewBehavior {
					public static class: java.lang.Class<com.telerik.widget.list.LoadOnDemandBehavior>;
					public setEnabled(param0: boolean): void;
					public onDetached(param0: com.telerik.widget.list.RadListView): void;
					public removeListener(param0: com.telerik.widget.list.LoadOnDemandBehavior.LoadOnDemandListener): void;
					public constructor(param0: globalAndroid.view.View, param1: globalAndroid.view.View);
					public setMaxRemainingItems(param0: number): void;
					public getMode(): com.telerik.widget.list.LoadOnDemandBehavior.LoadOnDemandMode;
					public setMode(param0: com.telerik.widget.list.LoadOnDemandBehavior.LoadOnDemandMode): void;
					public startLoad(): void;
					public addListener(param0: com.telerik.widget.list.LoadOnDemandBehavior.LoadOnDemandListener): void;
					public isInProgress(): boolean;
					public endLoad(): void;
					public constructor();
					public getMaxRemainingItems(): number;
					public isEnabled(): boolean;
					public onAttached(param0: com.telerik.widget.list.RadListView): void;
				}
				export module LoadOnDemandBehavior {
					export class LoadOnDemandListener extends java.lang.Object {
						public static class: java.lang.Class<com.telerik.widget.list.LoadOnDemandBehavior.LoadOnDemandListener>;
						/**
						 * Constructs a new instance of the com.telerik.widget.list.LoadOnDemandBehavior$LoadOnDemandListener interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
						 */
						public constructor(implementation: {
							onLoadStarted(): void;
							onLoadFinished(): void;
						});
						public constructor();
						public onLoadFinished(): void;
						public onLoadStarted(): void;
					}
					export class LoadOnDemandMode {
						public static class: java.lang.Class<com.telerik.widget.list.LoadOnDemandBehavior.LoadOnDemandMode>;
						public static MANUAL: com.telerik.widget.list.LoadOnDemandBehavior.LoadOnDemandMode;
						public static AUTOMATIC: com.telerik.widget.list.LoadOnDemandBehavior.LoadOnDemandMode;
						public static valueOf(param0: string): com.telerik.widget.list.LoadOnDemandBehavior.LoadOnDemandMode;
						public static valueOf(param0: java.lang.Class<any>, param1: string): java.lang.Enum<any>;
						public static values(): native.Array<com.telerik.widget.list.LoadOnDemandBehavior.LoadOnDemandMode>;
					}
					export class LoadingListener extends java.lang.Object {
						public static class: java.lang.Class<com.telerik.widget.list.LoadOnDemandBehavior.LoadingListener>;
						/**
						 * Constructs a new instance of the com.telerik.widget.list.LoadOnDemandBehavior$LoadingListener interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
						 */
						public constructor(implementation: {
							onLoadingRequested(): void;
							onLoadingFinished(): void;
						});
						public constructor();
						public onLoadingRequested(): void;
						public onLoadingFinished(): void;
					}
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class PerspectiveChangeInfo extends java.lang.Object {
					public static class: java.lang.Class<com.telerik.widget.list.PerspectiveChangeInfo>;
					public static DEFAULT_DURATION: number;
					public static DEFAULT_ALPHA: number;
					public static DEFAULT_TRANSLATION: number;
					public static DEFAULT_ELEVATION: number;
					public getAlpha(): number;
					public getTranslateTop(): number;
					public getTranslateStart(): number;
					public getElevation(): number;
					public setElevation(param0: number): void;
					public setTranslateEnd(param0: number): void;
					public constructor(param0: com.telerik.widget.list.DeckOfCardsLayoutManager);
					public setAlpha(param0: number): void;
					public setTranslateTop(param0: number): void;
					public getAnimationDuration(): number;
					public getTranslateEnd(): number;
					public setTranslateStart(param0: number): void;
					public setTranslateBottom(param0: number): void;
					public setAnimationDuration(param0: number): void;
					public getTranslateBottom(): number;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class RadListView extends globalAndroid.support.v7.widget.RecyclerView {
					public static class: java.lang.Class<com.telerik.widget.list.RadListView>;
					public invalidateChildInParent(param0: native.Array<number>, param1: globalAndroid.graphics.Rect): globalAndroid.view.ViewParent;
					public focusSearch(param0: number): globalAndroid.view.View;
					public focusableViewAvailable(param0: globalAndroid.view.View): void;
					public dispatchNestedPreScroll(param0: number, param1: number, param2: native.Array<number>, param3: native.Array<number>): boolean;
					public createContextMenu(param0: globalAndroid.view.ContextMenu): void;
					public computeHorizontalScrollRange(): number;
					public setEmptyContent(param0: globalAndroid.view.View): void;
					public isLayoutRequested(): boolean;
					public addIsEmptyChangedListener(param0: com.telerik.widget.list.RadListView.IsEmptyChangedListener): void;
					public onInterceptTouchEvent(param0: globalAndroid.view.MotionEvent): boolean;
					public removeIsEmptyChangedListener(param0: com.telerik.widget.list.RadListView.IsEmptyChangedListener): void;
					public dispatchDraw(param0: globalAndroid.graphics.Canvas): void;
					public scrollToPosition(param0: number): void;
					public constructor(param0: globalAndroid.content.Context, param1: globalAndroid.util.AttributeSet);
					public setEmptyContentEnabled(param0: boolean): void;
					public setFooterView(param0: globalAndroid.view.View): void;
					public dispatchNestedPreScroll(param0: number, param1: number, param2: native.Array<number>, param3: native.Array<number>, param4: number): boolean;
					public computeVerticalScrollExtent(): number;
					public stopNestedScroll(): void;
					public addView(param0: globalAndroid.view.View, param1: number, param2: number): void;
					public onKeyUp(param0: number, param1: globalAndroid.view.KeyEvent): boolean;
					public addView(param0: globalAndroid.view.View): void;
					public computeHorizontalScrollExtent(): number;
					public addView(param0: globalAndroid.view.View, param1: number, param2: globalAndroid.view.ViewGroup.LayoutParams): void;
					public focusSearch(param0: globalAndroid.view.View, param1: number): globalAndroid.view.View;
					public recomputeViewAttributes(param0: globalAndroid.view.View): void;
					public clearChildFocus(param0: globalAndroid.view.View): void;
					public getEmptyContent(): globalAndroid.view.View;
					public setHeaderView(param0: globalAndroid.view.View): void;
					public getChildVisibleRect(param0: globalAndroid.view.View, param1: globalAndroid.graphics.Rect, param2: globalAndroid.graphics.Point): boolean;
					public addBehavior(param0: com.telerik.widget.list.ListViewBehavior): void;
					public computeVerticalScrollOffset(): number;
					public removeItemClickListener(param0: com.telerik.widget.list.RadListView.ItemClickListener): void;
					public bringChildToFront(param0: globalAndroid.view.View): void;
					public dispatchNestedScroll(param0: number, param1: number, param2: number, param3: number, param4: native.Array<number>): boolean;
					public unscheduleDrawable(param0: globalAndroid.graphics.drawable.Drawable, param1: java.lang.Runnable): void;
					public removeBehavior(param0: com.telerik.widget.list.ListViewBehavior): void;
					public requestTransparentRegion(param0: globalAndroid.view.View): void;
					public onRestoreInstanceState(param0: globalAndroid.os.Parcelable): void;
					public onKeyLongPress(param0: number, param1: globalAndroid.view.KeyEvent): boolean;
					public childDrawableStateChanged(param0: globalAndroid.view.View): void;
					public onTouchEvent(param0: globalAndroid.view.MotionEvent): boolean;
					public onSaveInstanceState(): globalAndroid.os.Parcelable;
					public scheduleDrawable(param0: globalAndroid.graphics.drawable.Drawable, param1: java.lang.Runnable, param2: number): void;
					public requestFitSystemWindows(): void;
					public getGestureListener(): com.telerik.widget.list.ListViewGestureListener;
					public setLayoutManager(param0: globalAndroid.support.v7.widget.RecyclerView.LayoutManager): void;
					public getHeaderView(): globalAndroid.view.View;
					public getParent(): globalAndroid.view.ViewParent;
					public startActionModeForChild(param0: globalAndroid.view.View, param1: globalAndroid.view.ActionMode.Callback): globalAndroid.view.ActionMode;
					public swapAdapter(param0: globalAndroid.support.v7.widget.RecyclerView.Adapter<any>, param1: boolean): void;
					public stopNestedScroll(param0: number): void;
					public updateViewLayout(param0: globalAndroid.view.View, param1: globalAndroid.view.ViewGroup.LayoutParams): void;
					public requestChildFocus(param0: globalAndroid.view.View, param1: globalAndroid.view.View): void;
					public setItemAnimator(param0: globalAndroid.support.v7.widget.RecyclerView.ItemAnimator): void;
					public requestDisallowInterceptTouchEvent(param0: boolean): void;
					public hasNestedScrollingParent(param0: number): boolean;
					public addView(param0: globalAndroid.view.View, param1: number): void;
					public unscheduleDrawable(param0: globalAndroid.graphics.drawable.Drawable): void;
					public addView(param0: globalAndroid.view.View, param1: globalAndroid.view.ViewGroup.LayoutParams): void;
					public getChildAdapterPosition(param0: globalAndroid.view.View): number;
					public invalidateChild(param0: globalAndroid.view.View, param1: globalAndroid.graphics.Rect): void;
					public sendAccessibilityEvent(param0: number): void;
					public requestLayout(): void;
					public requestSendAccessibilityEvent(param0: globalAndroid.view.View, param1: globalAndroid.view.accessibility.AccessibilityEvent): boolean;
					public getParentForAccessibility(): globalAndroid.view.ViewParent;
					public setGestureListener(param0: com.telerik.widget.list.ListViewGestureListener): void;
					public onMeasure(param0: number, param1: number): void;
					public onKeyDown(param0: number, param1: globalAndroid.view.KeyEvent): boolean;
					public addItemClickListener(param0: com.telerik.widget.list.RadListView.ItemClickListener): void;
					public computeVerticalScrollRange(): number;
					public getFooterView(): globalAndroid.view.View;
					public setAdapter(param0: globalAndroid.support.v7.widget.RecyclerView.Adapter<any>): void;
					public onScrolled(param0: number, param1: number): void;
					public clearBehaviors(): void;
					public constructor(param0: globalAndroid.content.Context, param1: globalAndroid.util.AttributeSet, param2: number);
					public showContextMenuForChild(param0: globalAndroid.view.View): boolean;
					public sendAccessibilityEventUnchecked(param0: globalAndroid.view.accessibility.AccessibilityEvent): void;
					public scrollToPosition(param0: number, param1: number): void;
					public onKeyMultiple(param0: number, param1: number, param2: globalAndroid.view.KeyEvent): boolean;
					public removeView(param0: globalAndroid.view.View): void;
					public smoothScrollToPosition(param0: number): void;
					public constructor(param0: globalAndroid.content.Context);
					public scrollToStart(): void;
					public scrollToEnd(): void;
					public getAdapter(): globalAndroid.support.v7.widget.RecyclerView.Adapter<any>;
					public onLayout(param0: boolean, param1: number, param2: number, param3: number, param4: number): void;
					public startNestedScroll(param0: number, param1: number): boolean;
					public invalidateDrawable(param0: globalAndroid.graphics.drawable.Drawable): void;
					public computeHorizontalScrollOffset(): number;
					public startNestedScroll(param0: number): boolean;
					public hasNestedScrollingParent(): boolean;
					public isEmptyContentEnabled(): boolean;
					public smoothScrollToPosition(param0: number, param1: number): void;
					public requestChildRectangleOnScreen(param0: globalAndroid.view.View, param1: globalAndroid.graphics.Rect, param2: boolean): boolean;
					public dispatchNestedScroll(param0: number, param1: number, param2: number, param3: number, param4: native.Array<number>, param5: number): boolean;
				}
				export module RadListView {
					export class IsEmptyChangedListener extends java.lang.Object {
						public static class: java.lang.Class<com.telerik.widget.list.RadListView.IsEmptyChangedListener>;
						/**
						 * Constructs a new instance of the com.telerik.widget.list.RadListView$IsEmptyChangedListener interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
						 */
						public constructor(implementation: {
							onChanged(param0: boolean): void;
						});
						public constructor();
						public onChanged(param0: boolean): void;
					}
					export class ItemClickListener extends java.lang.Object {
						public static class: java.lang.Class<com.telerik.widget.list.RadListView.ItemClickListener>;
						/**
						 * Constructs a new instance of the com.telerik.widget.list.RadListView$ItemClickListener interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
						 */
						public constructor(implementation: {
							onItemClick(param0: number, param1: globalAndroid.view.MotionEvent): void;
							onItemLongClick(param0: number, param1: globalAndroid.view.MotionEvent): void;
						});
						public constructor();
						public onItemLongClick(param0: number, param1: globalAndroid.view.MotionEvent): void;
						public onItemClick(param0: number, param1: globalAndroid.view.MotionEvent): void;
					}
					export class ScrollToIndexLayoutListener extends java.lang.Object implements globalAndroid.view.View.OnLayoutChangeListener {
						public static class: java.lang.Class<com.telerik.widget.list.RadListView.ScrollToIndexLayoutListener>;
						public onLayoutChange(param0: globalAndroid.view.View, param1: number, param2: number, param3: number, param4: number, param5: number, param6: number, param7: number, param8: number): void;
						public constructor(param0: com.telerik.widget.list.RadListView, param1: number, param2: number);
					}
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class ReorderWithHandlesBehavior extends com.telerik.widget.list.ItemReorderBehavior {
					public static class: java.lang.Class<com.telerik.widget.list.ReorderWithHandlesBehavior>;
					public onDetached(param0: com.telerik.widget.list.RadListView): void;
					public endReorder(param0: boolean): void;
					public resolveHandleViewForCoordinates(param0: number, param1: number): globalAndroid.view.View;
					public onLongPress(param0: globalAndroid.view.MotionEvent): void;
					public isInProgress(): boolean;
					public onActionUpOrCancel(param0: boolean): boolean;
					public constructor();
					public onLongPressDragEnded(param0: boolean): boolean;
					public getReorderHandleOverride(param0: globalAndroid.view.ViewGroup): globalAndroid.view.View;
					public onLongPressDrag(param0: number, param1: number, param2: number, param3: number): void;
					public onAttached(param0: com.telerik.widget.list.RadListView): void;
					public onShortPressDrag(param0: number, param1: number, param2: number, param3: number): boolean;
					public constructor(param0: number);
					public onFling(param0: globalAndroid.view.MotionEvent, param1: globalAndroid.view.MotionEvent, param2: number, param3: number): boolean;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class ScaleItemAnimator extends com.telerik.widget.list.ListViewItemAnimator {
					public static class: java.lang.Class<com.telerik.widget.list.ScaleItemAnimator>;
					public getScaleY(): number;
					public animateViewAddedPrepare(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public onAnimationAddEnded(param0: globalAndroid.support.v4.view.ViewPropertyAnimatorCompat, param1: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public removeAnimation(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): globalAndroid.support.v4.view.ViewPropertyAnimatorCompat;
					public onEndAnimation(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public setScaleX(param0: number): void;
					public addAnimation(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): globalAndroid.support.v4.view.ViewPropertyAnimatorCompat;
					public getScaleX(): number;
					public constructor();
					public onAnimationRemoveEnded(param0: globalAndroid.support.v4.view.ViewPropertyAnimatorCompat, param1: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public endAnimation(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public setScaleY(param0: number): void;
					public onAnimationAddCancelled(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class SelectionBehavior extends com.telerik.widget.list.ListViewBehavior implements com.telerik.widget.list.ItemReorderBehavior.ItemReorderListener, com.telerik.widget.list.SwipeExecuteBehavior.SwipeExecuteListener, com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsListener {
					public static class: java.lang.Class<com.telerik.widget.list.SelectionBehavior>;
					public onSaveInstanceState(param0: globalAndroid.os.Parcelable): void;
					public onDetached(param0: com.telerik.widget.list.RadListView): void;
					public selectedItems(): java.util.List<any>;
					public onReorderFinished(): void;
					public onSwipeProgressChanged(param0: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionEvent): void;
					public getIsSelected(param0: number): boolean;
					public setSelectionOnLongPress(param0: com.telerik.widget.list.SelectionBehavior.SelectionOnTouch): void;
					public onSwipeStarted(param0: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionEvent): void;
					public changeIsSelected(param0: number, param1: boolean): void;
					public addListener(param0: com.telerik.widget.list.SelectionBehavior.SelectionChangedListener): void;
					public onSwipeEnded(param0: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionEvent): void;
					public onTapUp(param0: globalAndroid.view.MotionEvent): boolean;
					public constructor();
					public getSelectionOnLongPress(): com.telerik.widget.list.SelectionBehavior.SelectionOnTouch;
					public onSwipeStateChanged(param0: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsState, param1: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsState): void;
					public onSwipeStarted(param0: number): void;
					public onReorderStarted(param0: number): void;
					public onAttached(param0: com.telerik.widget.list.RadListView): void;
					public startSelection(): void;
					public getSelectionMode(): com.telerik.widget.list.SelectionBehavior.SelectionMode;
					public endSelection(): void;
					public setSelectionMode(param0: com.telerik.widget.list.SelectionBehavior.SelectionMode): void;
					public onExecuteFinished(param0: number): void;
					public removeListener(param0: com.telerik.widget.list.SelectionBehavior.SelectionChangedListener): void;
					public getSelectionOnTouch(): com.telerik.widget.list.SelectionBehavior.SelectionOnTouch;
					public getSelectedItemsSize(): number;
					public onReorderItem(param0: number, param1: number): void;
					public onSwipeProgressChanged(param0: number, param1: number, param2: globalAndroid.view.View): void;
					public onLongPress(param0: globalAndroid.view.MotionEvent): void;
					public onSwipeEnded(param0: number, param1: number): void;
					public isInProgress(): boolean;
					public onExecuteFinished(param0: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionEvent): void;
					public onRestoreInstanceState(param0: globalAndroid.os.Parcelable): void;
					public setSelectionOnTouch(param0: com.telerik.widget.list.SelectionBehavior.SelectionOnTouch): void;
					public changeIsSelected(param0: number): void;
				}
				export module SelectionBehavior {
					export class SelectionChangedListener extends java.lang.Object {
						public static class: java.lang.Class<com.telerik.widget.list.SelectionBehavior.SelectionChangedListener>;
						/**
						 * Constructs a new instance of the com.telerik.widget.list.SelectionBehavior$SelectionChangedListener interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
						 */
						public constructor(implementation: {
							onSelectionStarted(): void;
							onItemIsSelectedChanged(param0: number, param1: boolean): void;
							onSelectionEnded(): void;
						});
						public constructor();
						public onSelectionStarted(): void;
						public onSelectionEnded(): void;
						public onItemIsSelectedChanged(param0: number, param1: boolean): void;
					}
					export class SelectionMode {
						public static class: java.lang.Class<com.telerik.widget.list.SelectionBehavior.SelectionMode>;
						public static MULTIPLE: com.telerik.widget.list.SelectionBehavior.SelectionMode;
						public static SINGLE: com.telerik.widget.list.SelectionBehavior.SelectionMode;
						public static valueOf(param0: string): com.telerik.widget.list.SelectionBehavior.SelectionMode;
						public static valueOf(param0: java.lang.Class<any>, param1: string): java.lang.Enum<any>;
						public static values(): native.Array<com.telerik.widget.list.SelectionBehavior.SelectionMode>;
					}
					export class SelectionOnTouch {
						public static class: java.lang.Class<com.telerik.widget.list.SelectionBehavior.SelectionOnTouch>;
						public static NEVER: com.telerik.widget.list.SelectionBehavior.SelectionOnTouch;
						public static ALWAYS: com.telerik.widget.list.SelectionBehavior.SelectionOnTouch;
						public static AFTER_START: com.telerik.widget.list.SelectionBehavior.SelectionOnTouch;
						public static valueOf(param0: java.lang.Class<any>, param1: string): java.lang.Enum<any>;
						public static values(): native.Array<com.telerik.widget.list.SelectionBehavior.SelectionOnTouch>;
						public static valueOf(param0: string): com.telerik.widget.list.SelectionBehavior.SelectionOnTouch;
					}
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class SlideItemAnimator extends com.telerik.widget.list.ListViewItemAnimator {
					public static class: java.lang.Class<com.telerik.widget.list.SlideItemAnimator>;
					public static DIRECTION_LEFT: number;
					public static DIRECTION_TOP: number;
					public static DIRECTION_RIGHT: number;
					public static DIRECTION_BOTTOM: number;
					public setAnimateInDirection(param0: number): void;
					public animateViewAddedPrepare(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public onAnimationAddEnded(param0: globalAndroid.support.v4.view.ViewPropertyAnimatorCompat, param1: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public getAnimateInDirection(): number;
					public setAnimateOutDirection(param0: number): void;
					public constructor();
					public removeAnimation(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): globalAndroid.support.v4.view.ViewPropertyAnimatorCompat;
					public onAnimationRemoveEnded(param0: globalAndroid.support.v4.view.ViewPropertyAnimatorCompat, param1: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
					public getAnimateOutDirection(): number;
					public addAnimation(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): globalAndroid.support.v4.view.ViewPropertyAnimatorCompat;
					public onAnimationAddCancelled(param0: globalAndroid.support.v7.widget.RecyclerView.ViewHolder): void;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class SlideLayoutManager extends com.telerik.widget.list.SlideLayoutManagerBase {
					public static class: java.lang.Class<com.telerik.widget.list.SlideLayoutManager>;
					public static HORIZONTAL: number;
					public static VERTICAL: number;
					public scrollViews(param0: number, param1: number): void;
					public scaleXForIndex(param0: number): number;
					public previousItemsCount(): number;
					public isScrollOnTap(): boolean;
					public constructor(param0: globalAndroid.content.Context, param1: number);
					public alphaForIndex(param0: number): number;
					public setPreviousItemPreview(param0: number): void;
					public layoutView(param0: globalAndroid.view.View): void;
					public scaleYForIndex(param0: number): number;
					public setNextItemPreview(param0: number): void;
					public constructor(param0: globalAndroid.content.Context);
					public setScrollOnTap(param0: boolean): void;
					public calculateFrontViewSize(): void;
					public setItemSpacing(param0: number): void;
					public nextItemsCount(): number;
					public translationZForIndex(param0: number): number;
					public constructor();
					public getTransitionMode(): com.telerik.widget.list.SlideLayoutManager.Transition;
					public translationXForIndex(param0: number): number;
					public translationYForIndex(param0: number): number;
					public getNextItemPreview(): number;
					public getPreviousItemPreview(): number;
					public setTransitionMode(param0: com.telerik.widget.list.SlideLayoutManager.Transition): void;
					public getItemSpacing(): number;
				}
				export module SlideLayoutManager {
					export class Transition {
						public static class: java.lang.Class<com.telerik.widget.list.SlideLayoutManager.Transition>;
						public static SLIDE_AWAY: com.telerik.widget.list.SlideLayoutManager.Transition;
						public static SLIDE_OVER: com.telerik.widget.list.SlideLayoutManager.Transition;
						public static valueOf(param0: string): com.telerik.widget.list.SlideLayoutManager.Transition;
						public static valueOf(param0: java.lang.Class<any>, param1: string): java.lang.Enum<any>;
						public static values(): native.Array<com.telerik.widget.list.SlideLayoutManager.Transition>;
					}
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export abstract class SlideLayoutManagerBase extends globalAndroid.support.v7.widget.RecyclerView.LayoutManager {
					public static class: java.lang.Class<com.telerik.widget.list.SlideLayoutManagerBase>;
					public frontViewWidth: number;
					public frontViewHeight: number;
					public frontViewPosition: number;
					public scaleXForIndex(param0: number): number;
					public alphaForIndex(param0: number): number;
					public onItemsChanged(param0: globalAndroid.support.v7.widget.RecyclerView): void;
					public elevationForIndex(param0: number): number;
					public layoutView(param0: globalAndroid.view.View): void;
					public supportsPredictiveItemAnimations(): boolean;
					public fillAll(param0: globalAndroid.support.v7.widget.RecyclerView.Recycler, param1: globalAndroid.support.v7.widget.RecyclerView.State): void;
					public canScroll(param0: number): boolean;
					public nextIndex(param0: number): number;
					public scaleYForIndex(param0: number): number;
					public scrollToPosition(param0: number): void;
					public getStateItemCount(): number;
					public translationZForIndex(param0: number): number;
					public constructor();
					public calculateScrollProgress(): number;
					public translationXForIndex(param0: number): number;
					public translationYForIndex(param0: number): number;
					public generateDefaultLayoutParams(): globalAndroid.support.v7.widget.RecyclerView.LayoutParams;
					public isScrollEnabled(): boolean;
					public animationInterpolator(): globalAndroid.view.animation.Interpolator;
					public getOrientation(): number;
					public getDirection(param0: number): number;
					public setScrollEnabled(param0: boolean): void;
					public applyLayoutTransformations(param0: globalAndroid.view.View, param1: number, param2: boolean): void;
					public canScrollVertically(): boolean;
					public scrollViews(param0: number, param1: number): void;
					public onScrollStateChanged(param0: number): void;
					public setOrientation(param0: number): void;
					public onItemsUpdated(param0: globalAndroid.support.v7.widget.RecyclerView, param1: number, param2: number): void;
					public onItemsMoved(param0: globalAndroid.support.v7.widget.RecyclerView, param1: number, param2: number, param3: number): void;
					public canScrollHorizontally(): boolean;
					public layoutIndexForAdapterPosition(param0: number): number;
					public fillAtEnd(param0: globalAndroid.support.v7.widget.RecyclerView.Recycler, param1: globalAndroid.support.v7.widget.RecyclerView.State): void;
					public scrollVerticallyBy(param0: number, param1: globalAndroid.support.v7.widget.RecyclerView.Recycler, param2: globalAndroid.support.v7.widget.RecyclerView.State): number;
					public rotationXForIndex(param0: number): number;
					public addListener(param0: com.telerik.widget.list.CurrentPositionChangeListener): void;
					public onItemsUpdated(param0: globalAndroid.support.v7.widget.RecyclerView, param1: number, param2: number, param3: any): void;
					public onItemsAdded(param0: globalAndroid.support.v7.widget.RecyclerView, param1: number, param2: number): void;
					public scrollToPrevious(): void;
					public scrollHorizontallyBy(param0: number, param1: globalAndroid.support.v7.widget.RecyclerView.Recycler, param2: globalAndroid.support.v7.widget.RecyclerView.State): number;
					public findEndOffset(): number;
					public fillAtEnd(param0: globalAndroid.support.v7.widget.RecyclerView.Recycler, param1: globalAndroid.support.v7.widget.RecyclerView.State, param2: number): void;
					public onItemsRemoved(param0: globalAndroid.support.v7.widget.RecyclerView, param1: number, param2: number): void;
					public onLayoutChildren(param0: globalAndroid.support.v7.widget.RecyclerView.Recycler, param1: globalAndroid.support.v7.widget.RecyclerView.State): void;
					public updateViewLayoutParams(param0: globalAndroid.view.View, param1: number, param2: number): void;
					public calculateFrontViewSize(): void;
					public fill(param0: number, param1: globalAndroid.support.v7.widget.RecyclerView.Recycler, param2: globalAndroid.support.v7.widget.RecyclerView.State): void;
					public removeListener(param0: com.telerik.widget.list.CurrentPositionChangeListener): void;
					public getCurrentPosition(): number;
					public setCurrentPosition(param0: number): void;
					public fillAtStart(param0: globalAndroid.support.v7.widget.RecyclerView.Recycler, param1: globalAndroid.support.v7.widget.RecyclerView.State): void;
					public previousItemsCount(): number;
					public findStartOffset(): number;
					public scrollToNext(): void;
					public handleItemRemoved(param0: number, param1: globalAndroid.support.v7.widget.RecyclerView.Recycler, param2: globalAndroid.support.v7.widget.RecyclerView.State): void;
					public fillAtStart(param0: globalAndroid.support.v7.widget.RecyclerView.Recycler, param1: globalAndroid.support.v7.widget.RecyclerView.State, param2: number): void;
					public previousIndex(param0: number): number;
					public animationDuration(): number;
					public rotationForIndex(param0: number): number;
					public nextItemsCount(): number;
					public rotationYForIndex(param0: number): number;
					public onAdapterChanged(param0: globalAndroid.support.v7.widget.RecyclerView.Adapter<any>, param1: globalAndroid.support.v7.widget.RecyclerView.Adapter<any>): void;
					public notifyListeners(param0: number, param1: number): void;
					public adapterPositionForLayoutIndex(param0: number): number;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class SnappingSmoothScroller extends globalAndroid.support.v7.widget.LinearSmoothScroller {
					public static class: java.lang.Class<com.telerik.widget.list.SnappingSmoothScroller>;
					public static SNAP_NONE: number;
					public static SNAP_CENTER: number;
					public static SNAP_TOP: number;
					public static SNAP_BOTTOM: number;
					public computeScrollVectorForPosition(param0: number): globalAndroid.graphics.PointF;
					public getSnapMode(): number;
					public setSnapMode(param0: number): void;
					public calculateDtToFit(param0: number, param1: number, param2: number, param3: number, param4: number): number;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class StickyHeaderBehavior extends com.telerik.widget.list.ListViewBehavior {
					public static class: java.lang.Class<com.telerik.widget.list.StickyHeaderBehavior>;
					public stickyHeaderImage: globalAndroid.graphics.drawable.Drawable;
					public onDetached(param0: com.telerik.widget.list.RadListView): void;
					public onDispatchDraw(param0: globalAndroid.graphics.Canvas): void;
					public createImageFromView(param0: globalAndroid.view.View): globalAndroid.graphics.drawable.Drawable;
					public constructor();
					public onScrolled(param0: number, param1: number): void;
					public onAttached(param0: com.telerik.widget.list.RadListView): void;
					public getStickyImageForPosition(param0: number): globalAndroid.graphics.drawable.Drawable;
					public getViewForPosition(param0: number): globalAndroid.view.View;
					public getItemHeaderPosition(param0: number): number;
					public invalidate(): void;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class SwipeActionsBehavior extends com.telerik.widget.list.ListViewBehavior {
					public static class: java.lang.Class<com.telerik.widget.list.SwipeActionsBehavior>;
					public static DEFAULT_SWIPE_OFFSET: number;
					public static DEFAULT_SWIPE_LIMIT: number;
					public bindViewHolder(param0: com.telerik.widget.list.ListViewHolder, param1: number): void;
					public onDetached(param0: com.telerik.widget.list.RadListView): void;
					public addListener(param0: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsListener): void;
					public setSwipeLimitStart(param0: number): void;
					public onInterceptTouchEvent(param0: globalAndroid.view.MotionEvent): boolean;
					public endExecute(): void;
					public endExecute(param0: boolean): void;
					public getSwipeState(): com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsState;
					public onTapUp(param0: globalAndroid.view.MotionEvent): boolean;
					public constructor();
					public getDockMode(): com.telerik.widget.list.SwipeActionsBehavior.SwipeDockMode;
					public setSwipeThresholdStart(param0: number): void;
					public onAttached(param0: com.telerik.widget.list.RadListView): void;
					public setSwipeLimitEnd(param0: number): void;
					public managesViewHolders(): boolean;
					public onShortPressDrag(param0: number, param1: number, param2: number, param3: number): boolean;
					public createViewHolder(param0: globalAndroid.view.ViewGroup, param1: number): com.telerik.widget.list.ListViewHolder;
					public getSwipeLimitEnd(): number;
					public onLongPress(param0: globalAndroid.view.MotionEvent): void;
					public setSwipeThresholdEnd(param0: number): void;
					public isInProgress(): boolean;
					public onActionUpOrCancel(param0: boolean): boolean;
					public onLayout(param0: boolean, param1: number, param2: number, param3: number, param4: number): void;
					public removeListener(param0: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsListener): void;
					public getSwipeLimitStart(): number;
					public setDockMode(param0: com.telerik.widget.list.SwipeActionsBehavior.SwipeDockMode): void;
					public onFling(param0: globalAndroid.view.MotionEvent, param1: globalAndroid.view.MotionEvent, param2: number, param3: number): boolean;
				}
				export module SwipeActionsBehavior {
					export class DockContext extends java.lang.Object {
						public static class: java.lang.Class<com.telerik.widget.list.SwipeActionsBehavior.DockContext>;
					}
					export class SwipeActionEvent extends java.lang.Object {
						public static class: java.lang.Class<com.telerik.widget.list.SwipeActionsBehavior.SwipeActionEvent>;
						public swipeView(): globalAndroid.view.View;
						public swipedItemPosition(): number;
						public swipePositionWhenReleased(): number;
						public mainView(): globalAndroid.view.View;
						public isThresholdPassed(): boolean;
						public currentOffset(): number;
					}
					export class SwipeActionsListener extends java.lang.Object {
						public static class: java.lang.Class<com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsListener>;
						/**
						 * Constructs a new instance of the com.telerik.widget.list.SwipeActionsBehavior$SwipeActionsListener interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
						 */
						public constructor(implementation: {
							onSwipeStarted(param0: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionEvent): void;
							onSwipeProgressChanged(param0: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionEvent): void;
							onSwipeEnded(param0: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionEvent): void;
							onExecuteFinished(param0: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionEvent): void;
							onSwipeStateChanged(param0: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsState, param1: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsState): void;
						});
						public constructor();
						public onSwipeStarted(param0: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionEvent): void;
						public onSwipeEnded(param0: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionEvent): void;
						public onSwipeStateChanged(param0: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsState, param1: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsState): void;
						public onSwipeProgressChanged(param0: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionEvent): void;
						public onExecuteFinished(param0: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionEvent): void;
					}
					export class SwipeActionsState {
						public static class: java.lang.Class<com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsState>;
						public static IDLE: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsState;
						public static SWIPING: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsState;
						public static RESETTING: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsState;
						public static ACTIVE: com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsState;
						public static values(): native.Array<com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsState>;
						public static valueOf(param0: java.lang.Class<any>, param1: string): java.lang.Enum<any>;
						public static valueOf(param0: string): com.telerik.widget.list.SwipeActionsBehavior.SwipeActionsState;
					}
					export class SwipeDockMode {
						public static class: java.lang.Class<com.telerik.widget.list.SwipeActionsBehavior.SwipeDockMode>;
						public static DockAtLimit: com.telerik.widget.list.SwipeActionsBehavior.SwipeDockMode;
						public static DockAtThreshold: com.telerik.widget.list.SwipeActionsBehavior.SwipeDockMode;
						public static valueOf(param0: java.lang.Class<any>, param1: string): java.lang.Enum<any>;
						public static valueOf(param0: string): com.telerik.widget.list.SwipeActionsBehavior.SwipeDockMode;
						public static values(): native.Array<com.telerik.widget.list.SwipeActionsBehavior.SwipeDockMode>;
					}
					export class SwipeExecuteDataObserver extends globalAndroid.support.v7.widget.RecyclerView.AdapterDataObserver {
						public static class: java.lang.Class<com.telerik.widget.list.SwipeActionsBehavior.SwipeExecuteDataObserver>;
						public onChanged(): void;
						public onItemRangeRemoved(param0: number, param1: number): void;
					}
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class SwipeExecuteBehavior extends com.telerik.widget.list.ListViewBehavior {
					public static class: java.lang.Class<com.telerik.widget.list.SwipeExecuteBehavior>;
					public static DEFAULT_SWIPE_OFFSET: number;
					public static DEFAULT_SWIPE_LIMIT: number;
					public clearSwipeDrawables(): void;
					public onDetached(param0: com.telerik.widget.list.RadListView): void;
					public onDispatchDraw(param0: globalAndroid.graphics.Canvas): void;
					public setSwipeLimitStart(param0: number): void;
					public onInterceptTouchEvent(param0: globalAndroid.view.MotionEvent): boolean;
					public addSwipeDrawable(param0: number, param1: globalAndroid.graphics.drawable.Drawable): void;
					public endExecute(): void;
					public onTapUp(param0: globalAndroid.view.MotionEvent): boolean;
					public constructor();
					public startSwipe(param0: number, param1: number): void;
					public ensureWithinSwipeLimits(param0: number): number;
					public onAttached(param0: com.telerik.widget.list.RadListView): void;
					public setSwipeLimitEnd(param0: number): void;
					public onShortPressDrag(param0: number, param1: number, param2: number, param3: number): boolean;
					public removeSwipeDrawable(param0: number): boolean;
					public getSwipeOffset(): number;
					public getSwipeLimitEnd(): number;
					public removeListener(param0: com.telerik.widget.list.SwipeExecuteBehavior.SwipeExecuteListener): void;
					public onLongPress(param0: globalAndroid.view.MotionEvent): void;
					public moveSwipe(param0: number, param1: number, param2: number, param3: number): void;
					public isInProgress(): boolean;
					public setAutoDissolve(param0: boolean): void;
					public endSwipe(): void;
					public addListener(param0: com.telerik.widget.list.SwipeExecuteBehavior.SwipeExecuteListener): void;
					public onActionUpOrCancel(param0: boolean): boolean;
					public createSwipeImage(param0: globalAndroid.view.View): globalAndroid.graphics.drawable.Drawable;
					public setSwipeOffset(param0: number): void;
					public isAutoDissolve(): boolean;
					public getSwipeLimitStart(): number;
					public onFling(param0: globalAndroid.view.MotionEvent, param1: globalAndroid.view.MotionEvent, param2: number, param3: number): boolean;
				}
				export module SwipeExecuteBehavior {
					export class EventInfo extends java.lang.Object {
						public static class: java.lang.Class<com.telerik.widget.list.SwipeExecuteBehavior.EventInfo>;
					}
					export class SwipeExecuteDataObserver extends globalAndroid.support.v7.widget.RecyclerView.AdapterDataObserver {
						public static class: java.lang.Class<com.telerik.widget.list.SwipeExecuteBehavior.SwipeExecuteDataObserver>;
						public onChanged(): void;
						public onItemRangeRemoved(param0: number, param1: number): void;
					}
					export class SwipeExecuteDismissedListener extends java.lang.Object {
						public static class: java.lang.Class<com.telerik.widget.list.SwipeExecuteBehavior.SwipeExecuteDismissedListener>;
						/**
						 * Constructs a new instance of the com.telerik.widget.list.SwipeExecuteBehavior$SwipeExecuteDismissedListener interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
						 */
						public constructor(implementation: {
							onSwipeContentDismissed(): void;
						});
						public constructor();
						public onSwipeContentDismissed(): void;
					}
					export class SwipeExecuteListener extends java.lang.Object {
						public static class: java.lang.Class<com.telerik.widget.list.SwipeExecuteBehavior.SwipeExecuteListener>;
						/**
						 * Constructs a new instance of the com.telerik.widget.list.SwipeExecuteBehavior$SwipeExecuteListener interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
						 */
						public constructor(implementation: {
							onSwipeStarted(param0: number): void;
							onSwipeProgressChanged(param0: number, param1: number, param2: globalAndroid.view.View): void;
							onSwipeEnded(param0: number, param1: number): void;
							onExecuteFinished(param0: number): void;
						});
						public constructor();
						public onSwipeProgressChanged(param0: number, param1: number, param2: globalAndroid.view.View): void;
						public onSwipeEnded(param0: number, param1: number): void;
						public onSwipeStarted(param0: number): void;
						public onExecuteFinished(param0: number): void;
					}
					export class SwipeState {
						public static class: java.lang.Class<com.telerik.widget.list.SwipeExecuteBehavior.SwipeState>;
						public static IDLE: com.telerik.widget.list.SwipeExecuteBehavior.SwipeState;
						public static STARTED: com.telerik.widget.list.SwipeExecuteBehavior.SwipeState;
						public static ENDED: com.telerik.widget.list.SwipeExecuteBehavior.SwipeState;
						public static valueOf(param0: java.lang.Class<any>, param1: string): java.lang.Enum<any>;
						public static valueOf(param0: string): com.telerik.widget.list.SwipeExecuteBehavior.SwipeState;
						public static values(): native.Array<com.telerik.widget.list.SwipeExecuteBehavior.SwipeState>;
					}
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class SwipeLayout extends globalAndroid.view.ViewGroup {
					public static class: java.lang.Class<com.telerik.widget.list.SwipeLayout>;
					public invalidateChildInParent(param0: native.Array<number>, param1: globalAndroid.graphics.Rect): globalAndroid.view.ViewParent;
					public focusSearch(param0: number): globalAndroid.view.View;
					public focusableViewAvailable(param0: globalAndroid.view.View): void;
					public createContextMenu(param0: globalAndroid.view.ContextMenu): void;
					public isLayoutRequested(): boolean;
					public generateLayoutParams(param0: globalAndroid.view.ViewGroup.LayoutParams): globalAndroid.view.ViewGroup.LayoutParams;
					public constructor(param0: globalAndroid.content.Context, param1: globalAndroid.util.AttributeSet);
					public addView(param0: globalAndroid.view.View, param1: number, param2: number): void;
					public onKeyUp(param0: number, param1: globalAndroid.view.KeyEvent): boolean;
					public addView(param0: globalAndroid.view.View): void;
					public addView(param0: globalAndroid.view.View, param1: number, param2: globalAndroid.view.ViewGroup.LayoutParams): void;
					public focusSearch(param0: globalAndroid.view.View, param1: number): globalAndroid.view.View;
					public checkLayoutParams(param0: globalAndroid.view.ViewGroup.LayoutParams): boolean;
					public setMainView(param0: globalAndroid.view.View): void;
					public recomputeViewAttributes(param0: globalAndroid.view.View): void;
					public clearChildFocus(param0: globalAndroid.view.View): void;
					public getChildVisibleRect(param0: globalAndroid.view.View, param1: globalAndroid.graphics.Rect, param2: globalAndroid.graphics.Point): boolean;
					public bringChildToFront(param0: globalAndroid.view.View): void;
					public unscheduleDrawable(param0: globalAndroid.graphics.drawable.Drawable, param1: java.lang.Runnable): void;
					public requestTransparentRegion(param0: globalAndroid.view.View): void;
					public onKeyLongPress(param0: number, param1: globalAndroid.view.KeyEvent): boolean;
					public childDrawableStateChanged(param0: globalAndroid.view.View): void;
					public scheduleDrawable(param0: globalAndroid.graphics.drawable.Drawable, param1: java.lang.Runnable, param2: number): void;
					public requestFitSystemWindows(): void;
					public getParent(): globalAndroid.view.ViewParent;
					public startActionModeForChild(param0: globalAndroid.view.View, param1: globalAndroid.view.ActionMode.Callback): globalAndroid.view.ActionMode;
					public updateViewLayout(param0: globalAndroid.view.View, param1: globalAndroid.view.ViewGroup.LayoutParams): void;
					public requestChildFocus(param0: globalAndroid.view.View, param1: globalAndroid.view.View): void;
					public requestDisallowInterceptTouchEvent(param0: boolean): void;
					public addView(param0: globalAndroid.view.View, param1: number): void;
					public unscheduleDrawable(param0: globalAndroid.graphics.drawable.Drawable): void;
					public addView(param0: globalAndroid.view.View, param1: globalAndroid.view.ViewGroup.LayoutParams): void;
					public invalidateChild(param0: globalAndroid.view.View, param1: globalAndroid.graphics.Rect): void;
					public sendAccessibilityEvent(param0: number): void;
					public requestLayout(): void;
					public requestSendAccessibilityEvent(param0: globalAndroid.view.View, param1: globalAndroid.view.accessibility.AccessibilityEvent): boolean;
					public getParentForAccessibility(): globalAndroid.view.ViewParent;
					public onMeasure(param0: number, param1: number): void;
					public onKeyDown(param0: number, param1: globalAndroid.view.KeyEvent): boolean;
					public generateLayoutParams(param0: globalAndroid.util.AttributeSet): globalAndroid.view.ViewGroup.LayoutParams;
					public constructor(param0: globalAndroid.content.Context, param1: globalAndroid.util.AttributeSet, param2: number);
					public showContextMenuForChild(param0: globalAndroid.view.View): boolean;
					public sendAccessibilityEventUnchecked(param0: globalAndroid.view.accessibility.AccessibilityEvent): void;
					public onKeyMultiple(param0: number, param1: number, param2: globalAndroid.view.KeyEvent): boolean;
					public removeView(param0: globalAndroid.view.View): void;
					public constructor(param0: globalAndroid.content.Context);
					public setSwipeView(param0: globalAndroid.view.View): void;
					public shouldDelayChildPressedState(): boolean;
					public onLayout(param0: boolean, param1: number, param2: number, param3: number, param4: number): void;
					public invalidateDrawable(param0: globalAndroid.graphics.drawable.Drawable): void;
					public requestChildRectangleOnScreen(param0: globalAndroid.view.View, param1: globalAndroid.graphics.Rect, param2: boolean): boolean;
					public static layoutChild(param0: globalAndroid.view.View, param1: number, param2: number, param3: number, param4: number): void;
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class SwipeRefreshBehavior extends com.telerik.widget.list.ListViewBehavior {
					public static class: java.lang.Class<com.telerik.widget.list.SwipeRefreshBehavior>;
					public endRefresh(param0: boolean): void;
					public removeListener(param0: com.telerik.widget.list.SwipeRefreshBehavior.SwipeRefreshListener): void;
					public onDetached(param0: com.telerik.widget.list.RadListView): void;
					public startRefresh(): void;
					public init(param0: globalAndroid.content.Context): void;
					public owner(): com.telerik.widget.list.RadListView;
					public addListener(param0: com.telerik.widget.list.SwipeRefreshBehavior.SwipeRefreshListener): void;
					public onLongPress(param0: globalAndroid.view.MotionEvent): void;
					public isInProgress(): boolean;
					public onActionUpOrCancel(param0: boolean): boolean;
					public constructor();
					public onLayout(param0: boolean, param1: number, param2: number, param3: number, param4: number): void;
					public insertRefreshLayout(param0: com.telerik.widget.list.RadListView, param1: globalAndroid.support.v4.widget.SwipeRefreshLayout): void;
					public onAttached(param0: com.telerik.widget.list.RadListView): void;
					public swipeRefresh(): globalAndroid.support.v4.widget.SwipeRefreshLayout;
				}
				export module SwipeRefreshBehavior {
					export class RefreshListener extends java.lang.Object {
						public static class: java.lang.Class<com.telerik.widget.list.SwipeRefreshBehavior.RefreshListener>;
						/**
						 * Constructs a new instance of the com.telerik.widget.list.SwipeRefreshBehavior$RefreshListener interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
						 */
						public constructor(implementation: {
							onRefreshFinished(): void;
						});
						public constructor();
						public onRefreshFinished(): void;
					}
					export class SwipeRefreshIndicator extends globalAndroid.support.v4.widget.SwipeRefreshLayout {
						public static class: java.lang.Class<com.telerik.widget.list.SwipeRefreshBehavior.SwipeRefreshIndicator>;
						public isLayoutRequested(): boolean;
						public dispatchNestedPreScroll(param0: number, param1: number, param2: native.Array<number>, param3: native.Array<number>): boolean;
						public constructor(param0: globalAndroid.content.Context);
						public sendAccessibilityEvent(param0: number): void;
						public onStartNestedScroll(param0: globalAndroid.view.View, param1: globalAndroid.view.View, param2: number): boolean;
						public sendAccessibilityEventUnchecked(param0: globalAndroid.view.accessibility.AccessibilityEvent): void;
						public clearChildFocus(param0: globalAndroid.view.View): void;
						public requestChildFocus(param0: globalAndroid.view.View, param1: globalAndroid.view.View): void;
						public onNestedFling(param0: globalAndroid.view.View, param1: number, param2: number, param3: boolean): boolean;
						public dispatchNestedPreFling(param0: number, param1: number): boolean;
						public dispatchNestedScroll(param0: number, param1: number, param2: number, param3: number, param4: native.Array<number>): boolean;
						public invalidateChild(param0: globalAndroid.view.View, param1: globalAndroid.graphics.Rect): void;
						public getNestedScrollAxes(): number;
						public addView(param0: globalAndroid.view.View, param1: number, param2: number): void;
						public onMeasure(param0: number, param1: number): void;
						public setNestedScrollingEnabled(param0: boolean): void;
						public onKeyMultiple(param0: number, param1: number, param2: globalAndroid.view.KeyEvent): boolean;
						public hasNestedScrollingParent(): boolean;
						public onTouchEvent(param0: globalAndroid.view.MotionEvent): boolean;
						public removeView(param0: globalAndroid.view.View): void;
						public getChildVisibleRect(param0: globalAndroid.view.View, param1: globalAndroid.graphics.Rect, param2: globalAndroid.graphics.Point): boolean;
						public onKeyUp(param0: number, param1: globalAndroid.view.KeyEvent): boolean;
						public isNestedScrollingEnabled(): boolean;
						public onNestedPreScroll(param0: globalAndroid.view.View, param1: number, param2: number, param3: native.Array<number>): void;
						public recomputeViewAttributes(param0: globalAndroid.view.View): void;
						public showContextMenuForChild(param0: globalAndroid.view.View): boolean;
						public unscheduleDrawable(param0: globalAndroid.graphics.drawable.Drawable): void;
						public requestDisallowInterceptTouchEvent(param0: boolean): void;
						public invalidateChildInParent(param0: native.Array<number>, param1: globalAndroid.graphics.Rect): globalAndroid.view.ViewParent;
						public startNestedScroll(param0: number): boolean;
						public onNestedScroll(param0: globalAndroid.view.View, param1: number, param2: number, param3: number, param4: number): void;
						public addView(param0: globalAndroid.view.View, param1: globalAndroid.view.ViewGroup.LayoutParams): void;
						public onKeyLongPress(param0: number, param1: globalAndroid.view.KeyEvent): boolean;
						public onKeyDown(param0: number, param1: globalAndroid.view.KeyEvent): boolean;
						public requestLayout(): void;
						public bringChildToFront(param0: globalAndroid.view.View): void;
						public startActionModeForChild(param0: globalAndroid.view.View, param1: globalAndroid.view.ActionMode.Callback): globalAndroid.view.ActionMode;
						public addView(param0: globalAndroid.view.View, param1: number): void;
						public constructor(param0: com.telerik.widget.list.SwipeRefreshBehavior, param1: globalAndroid.content.Context);
						public requestChildRectangleOnScreen(param0: globalAndroid.view.View, param1: globalAndroid.graphics.Rect, param2: boolean): boolean;
						public focusSearch(param0: globalAndroid.view.View, param1: number): globalAndroid.view.View;
						public onStopNestedScroll(param0: globalAndroid.view.View): void;
						public dispatchNestedFling(param0: number, param1: number, param2: boolean): boolean;
						public invalidateDrawable(param0: globalAndroid.graphics.drawable.Drawable): void;
						public requestTransparentRegion(param0: globalAndroid.view.View): void;
						public addView(param0: globalAndroid.view.View, param1: number, param2: globalAndroid.view.ViewGroup.LayoutParams): void;
						public addView(param0: globalAndroid.view.View): void;
						public onInterceptTouchEvent(param0: globalAndroid.view.MotionEvent): boolean;
						public onNestedPreFling(param0: globalAndroid.view.View, param1: number, param2: number): boolean;
						public createContextMenu(param0: globalAndroid.view.ContextMenu): void;
						public constructor(param0: globalAndroid.content.Context, param1: globalAndroid.util.AttributeSet);
						public childDrawableStateChanged(param0: globalAndroid.view.View): void;
						public unscheduleDrawable(param0: globalAndroid.graphics.drawable.Drawable, param1: java.lang.Runnable): void;
						public requestFitSystemWindows(): void;
						public stopNestedScroll(): void;
						public updateViewLayout(param0: globalAndroid.view.View, param1: globalAndroid.view.ViewGroup.LayoutParams): void;
						public getParentForAccessibility(): globalAndroid.view.ViewParent;
						public scheduleDrawable(param0: globalAndroid.graphics.drawable.Drawable, param1: java.lang.Runnable, param2: number): void;
						public focusableViewAvailable(param0: globalAndroid.view.View): void;
						public focusSearch(param0: number): globalAndroid.view.View;
						public requestSendAccessibilityEvent(param0: globalAndroid.view.View, param1: globalAndroid.view.accessibility.AccessibilityEvent): boolean;
						public onNestedScrollAccepted(param0: globalAndroid.view.View, param1: globalAndroid.view.View, param2: number): void;
						public constructor(param0: globalAndroid.content.Context, param1: globalAndroid.util.AttributeSet, param2: number);
						public getParent(): globalAndroid.view.ViewParent;
					}
					export class SwipeRefreshListener extends java.lang.Object {
						public static class: java.lang.Class<com.telerik.widget.list.SwipeRefreshBehavior.SwipeRefreshListener>;
						/**
						 * Constructs a new instance of the com.telerik.widget.list.SwipeRefreshBehavior$SwipeRefreshListener interface with the provided implementation. An empty constructor exists calling super() when extending the interface class.
						 */
						public constructor(implementation: {
							onRefreshRequested(): void;
						});
						public constructor();
						public onRefreshRequested(): void;
					}
				}
			}
		}
	}
}

declare module com {
	export module telerik {
		export module widget {
			export module list {
				export class WrapLayoutManager extends globalAndroid.support.v7.widget.RecyclerView.LayoutManager {
					public static class: java.lang.Class<com.telerik.widget.list.WrapLayoutManager>;
					public static HORIZONTAL: number;
					public static VERTICAL: number;
					public getGravity(): number;
					public constructor(param0: globalAndroid.content.Context, param1: number);
					public onItemsRemoved(param0: globalAndroid.support.v7.widget.RecyclerView, param1: number, param2: number): void;
					public onItemsChanged(param0: globalAndroid.support.v7.widget.RecyclerView): void;
					public onLayoutChildren(param0: globalAndroid.support.v7.widget.RecyclerView.Recycler, param1: globalAndroid.support.v7.widget.RecyclerView.State): void;
					public computeHorizontalScrollExtent(param0: globalAndroid.support.v7.widget.RecyclerView.State): number;
					public scrollToPosition(param0: number): void;
					public computeHorizontalScrollOffset(param0: globalAndroid.support.v7.widget.RecyclerView.State): number;
					public constructor();
					public computeVerticalScrollExtent(param0: globalAndroid.support.v7.widget.RecyclerView.State): number;
					public generateDefaultLayoutParams(): globalAndroid.support.v7.widget.RecyclerView.LayoutParams;
					public getLineSpacing(): number;
					public computeVerticalScrollRange(param0: globalAndroid.support.v7.widget.RecyclerView.State): number;
					public canScrollVertically(): boolean;
					public setMinimumItemSpacing(param0: number): void;
					public setGravity(param0: number): void;
					public computeVerticalScrollOffset(param0: globalAndroid.support.v7.widget.RecyclerView.State): number;
					public onItemsMoved(param0: globalAndroid.support.v7.widget.RecyclerView, param1: number, param2: number, param3: number): void;
					public computeHorizontalScrollRange(param0: globalAndroid.support.v7.widget.RecyclerView.State): number;
					public constructor(param0: globalAndroid.content.Context);
					public canScrollHorizontally(): boolean;
					public getMinimumItemSpacing(): number;
					public scrollVerticallyBy(param0: number, param1: globalAndroid.support.v7.widget.RecyclerView.Recycler, param2: globalAndroid.support.v7.widget.RecyclerView.State): number;
					public constructor(param0: globalAndroid.content.Context, param1: globalAndroid.util.AttributeSet, param2: number, param3: number);
					public onAdapterChanged(param0: globalAndroid.support.v7.widget.RecyclerView.Adapter<any>, param1: globalAndroid.support.v7.widget.RecyclerView.Adapter<any>): void;
					public onItemsAdded(param0: globalAndroid.support.v7.widget.RecyclerView, param1: number, param2: number): void;
					public setLineSpacing(param0: number): void;
					public scrollHorizontallyBy(param0: number, param1: globalAndroid.support.v7.widget.RecyclerView.Recycler, param2: globalAndroid.support.v7.widget.RecyclerView.State): number;
				}
			}
		}
	}
}

//Generics information:
//com.telerik.android.data.AndroidDataSourceAdapter:1
//com.telerik.android.data.CurrencyService:1
//com.telerik.android.data.CurrentItemChangedInfo:1
//com.telerik.android.data.CurrentItemChangedListener:1
//com.telerik.android.data.DataChangeInfo:1
//com.telerik.android.data.DataChangedListener:1
//com.telerik.android.data.DataItem:1
//com.telerik.android.data.DataSourceAdapterBase:1
//com.telerik.android.data.RadDataSource:1
//com.telerik.android.data.RadDataSourceAdapter:1
//com.telerik.android.data.SelectionChangeInfo:1
//com.telerik.android.data.SelectionChangeListener:1
//com.telerik.android.data.SelectionService:1
//com.telerik.widget.list.DefaultSelectionAdapter:1