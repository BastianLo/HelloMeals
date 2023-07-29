declare module '*.vue' {
    import {DefineComponent} from 'vue';
    const component: DefineComponent<{}, {}, any> & {
        $t: (key: string) => string;
    };
    export default component;
}
