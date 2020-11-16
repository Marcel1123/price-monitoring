package aspects;

public aspect TraceMonitoringAspect {
    private int callDepth = -1;

    pointcut tracePoints(): !within(TraceMonitoringAspect);

    before(): tracePoints() {
        callDepth++;
        print("Before", thisJoinPoint);
    }

    after () : tracePoints() {
        print("After", thisJoinPoint);
        callDepth--;
    }

    private void print(String prefix, Object message){
        for(int i = 0, spaces = callDepth * 2; i < spaces; i++){
            System.out.println(" ");
        }
        System.out.println(prefix + ": " + message);
    }
}
