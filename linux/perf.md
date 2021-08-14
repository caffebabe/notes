## perf_events
perf_events is an event-oriented observability tool, which can help you solve advanced performance and troubleshooting functions. Questions that can be answered include:
- Why is the kernel on-CPU so much? What code-paths?
- Which code-paths are causing CPU level 2 cache misses?
- Are the CPUs stalled on memory I/O?
- Which code-paths are allocating memory, and how much?
- What is triggering TCP retransmits?
- Is a certain kernel function being called, and how often?
- What reasons are threads leaving the CPU?

## Events
perf_events instruments "events", which are a unified interface for different kernel instrumentation frameworks. 
![](img/perf_events_map.png)

The types of events are:
- Hardware Events: CPU performance monitoring counters.
- Software Events: These are low level events based on kernel counters. For example, CPU migrations, minor faults, major faults, etc.
- Kernel Tracepoint Events: This are static kernel-level instrumentation points that are hardcoded in interesting and logical places in the kernel.
- User Statically-Defined Tracing (USDT): These are static tracepoints for user-level programs and applications.
- Dynamic Tracing: Software can be dynamically instrumented, creating events in any location. For kernel software, this uses the kprobes framework. For user-level software, uprobes.
- Timed Profiling: Snapshots can be collected at an arbitrary frequency, using perf record -FHz. This is commonly used for CPU usage profiling, and works by creating custom timed interrupt events.

[大神原文](http://www.brendangregg.com/perf.html)



