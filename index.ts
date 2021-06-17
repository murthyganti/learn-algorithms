import { defer, timer, Subject } from 'rxjs';
import { map, switchMap, tap, take } from 'rxjs/operators';

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
        return timer(1000).pipe(
          take(1),
          map(() => 'INITIALIZED')
        );
      case 2:
        return timer(1000).pipe(
          take(1),
          map(() => 'PENDING')
        );
      default:
        return timer(1000).pipe(
          take(1),
          map(() => 'COMPLETE')
        );
    }
  };
})();

/**
 * This function represents some kind of blocking network-related operation (eg. checking the status of an operation and only proceeding if/when a particular status is returned).
 */
const doNetworkyThing = () => {
  // Here we use `defer()` to ensure that the polling behaviour is not triggered until the
  // stream consumer actually subscribes.
  return defer(() => {
    const isComplete$ = new Subject();
    const loop$ = new Subject();

    // The loop works like so:
    // - It is seeded with an initial value.
    // - Each time the stream emits a new value, the polling behaviour is triggered.
    // - The polling behaviour returns a status.
    // - If the status is 'COMPLETE', then both the loop completes.
    // - Additionally, the `isComplete$` emits and completes.
    // - If the status is not complete then it emits another value (kicking off the process again).
    loop$
      .pipe(
        switchMap(() => {
          console.log('__ FETCHING DATA');
          return poll();
        }),
        tap(status => {
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
        })
      )
      .subscribe();

    loop$.next();

    return isComplete$;
  });
};
