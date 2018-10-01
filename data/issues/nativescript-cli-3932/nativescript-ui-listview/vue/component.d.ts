import { ListViewItemSnapMode } from '../';
declare const _default: {
    props: {
        items: {
            type: ArrayConstructor;
            required: boolean;
        };
        '+alias': {
            type: StringConstructor;
            default: string;
        };
        '+index': {
            type: StringConstructor;
        };
        layout: {
            type: StringConstructor;
            default: string;
        };
        orientation: {
            type: StringConstructor;
            default: string;
        };
        gridSpanCount: {
            type: NumberConstructor;
            default: number;
        };
        itemHeight: {
            type: StringConstructor;
            default: string;
        };
        itemTemplateSelector: {
            type: FunctionConstructor;
            default: any;
        };
    };
    template: string;
    computed: {
        scrollDirection(): "Vertical" | "Horizontal";
    };
    watch: {
        items: {
            handler(newVal: any): void;
            deep: boolean;
        };
    };
    created(): void;
    mounted(): void;
    methods: {
        onItemTap(args: any): void;
        onItemLoading(args: any): void;
        refresh(): void;
        scrollToIndex(index: Number, animate?: Boolean, snapMode?: ListViewItemSnapMode): void;
        notifySwipeToExecuteFinished(): void;
        getSelectedItems(): any;
    };
};
export default _default;
