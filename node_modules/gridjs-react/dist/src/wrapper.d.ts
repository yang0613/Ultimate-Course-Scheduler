import { Component as gComponent } from "gridjs";
export declare class ReactWrapper extends gComponent<{
    element: any;
    parent?: string;
}> {
    static defaultProps: {
        parent: string;
    };
    ref: import("preact").RefObject<any>;
    componentDidMount(): void;
    render(): import("preact").VNode<any>;
}
export declare function _(element: any, parent?: string): import("preact").VNode<any>;
