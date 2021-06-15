(function(System, SystemJS) {(function (require, exports, module, __filename, __dirname, global, GLOBAL, process, Buffer) {"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const rxjs_1 = require("rxjs");
const operators_1 = require("rxjs/operators");
/**
 * This function _simulates_ some kind of polling-type behaviour. More specifically,
 * it simulates the scenario where polling is expected to yield different results over time,
 * and where one of those results signifies completion.
 */
const poll = (() => {
    let counter = 0;
    return () => {
        switch (++counter) {
            case 1:
                return rxjs_1.timer(1000).pipe(operators_1.take(1), operators_1.map(() => 'INITIALIZED'));
            case 2:
                return rxjs_1.timer(1000).pipe(operators_1.take(1), operators_1.map(() => 'PENDING'));
            default:
                return rxjs_1.timer(1000).pipe(operators_1.take(1), operators_1.map(() => 'COMPLETE'));
        }
    };
})();
/**
 * This function represents some kind of blocking network-related operation (eg. checking the status of an operation and only proceeding if/when a particular status is returned).
 */
const doNetworkyThing = () => {
    // Here we use `defer()` to ensure that the polling behaviour is not triggered until the
    // stream consumer actually subscribes.
    return rxjs_1.defer(() => {
        const isComplete$ = new rxjs_1.Subject();
        const loop$ = new rxjs_1.Subject();
        // The loop works like so:
        // - It is seeded with an initial value.
        // - Each time the stream emits a new value, the polling behaviour is triggered.
        // - The polling behaviour returns a status.
        // - If the status is 'COMPLETE', then both the loop completes.
        // - Additionally, the `isComplete$` emits and completes.
        // - If the status is not complete then it emits another value (kicking off the process again).
        loop$
            .pipe(operators_1.switchMap(() => {
            console.log('__ FETCHING DATA');
            return poll();
        }), operators_1.tap(status => {
            console.log('__ EVALUATING RESPONSE');
            switch (status) {
                case 'COMPLETE': {
                    console.log('__ IS COMPLETE');
                    loop$.complete();
                    isComplete$.next();
                    break;
                }
                default: {
                    console.log('__ IS NOT COMPLETE');
                    loop$.next();
                }
            }
        }))
            .subscribe();
        loop$.next();
        return isComplete$;
    });
};
// Init.
doNetworkyThing().subscribe(() => console.log('__ COMPLETED NETWORKY THING'));

}).apply(__cjsWrapper.exports, __cjsWrapper.args);
})(System, System);