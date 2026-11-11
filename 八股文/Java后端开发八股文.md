## 一、Java 基础

### Q001 ★★★ 极高 `==` 和 equals 的区别？

`==` 比较的是引用（地址）或基本类型的值；equals 是方法，默认实现等价于 `==`，但 String、包装类、集合类都重写成了「比较内容」，所以对象比较必须用 equals。

- `==`：基本类型比数值，引用类型比是否指向同一个对象。
- equals：Object 里的原始实现就是 this `==` obj；重写后按业务字段比较内容。
- 实操原则：判断「是不是同一个对象」用 `==`，判断「值是否相等」用 equals；字符串常量建议反过来写 "abc".equals(s) 避免 NPE。
- 两者不等价的地方：两个 new String("abc") 用 `==` 是 false，用 equals 是 true。
- 和 hashCode 的关系见下一题，面试官几乎必然连着追问。

> **记忆点**：`==` 看地址，equals 看内容；基本类型只认 `==`。

#### 追问：为什么 equals 相等的对象 hashCode 必须相等？

因为哈希容器（HashMap/HashSet）先用 hashCode 定位桶，再用 equals 在桶内找。如果两个相等对象哈希值不同，它们会被放进不同的桶，get 就永远找不到。反过来 hashCode 相等但 equals 不等是允许的（哈希冲突），只是会退化成链表，影响性能。

### Q002 ★★★ 高 hashCode 与 equals 的约定是什么？只重写一个会怎样？

约定是「equals 相等则 hashCode 必须相等」，所以重写 equals 必须重写 hashCode；只重写 equals 会让 HashMap / HashSet 出现「存进去取不出来」和「重复元素」的问题。

- 三条契约：自反、对称、传递；equals 相等 → hashCode 相等（必要不充分）。
- 只重写 equals 的后果：两个「相等」对象哈希值不同，落进不同桶，set.add 加得进去、map.get 取不出来。
- 只重写 hashCode 的后果：哈希碰撞时用默认 equals（地址比较）判不相等，容器里出现「逻辑重复」的元素。
- 正确做法：用 IDE / Lombok @EqualsAndHashCode 生成，或记录类（record）自动生成。
- 字段选择上，参与 equals 的字段必须参与 hashCode；可变字段不要参与，否则对象入集合后哈希变了就找不回。

> **记忆点**：equals 相等 → hash 相等；hash 相等 ⇏ equals 相等（这叫哈希冲突）。

#### 追问：HashMap 里 key 是可变对象会怎样？

入表时按当时的哈希值定位。之后修改了参与哈希计算的字段，再 get 会用新哈希值去另一个桶找，原值就丢了（内存泄漏）。所以 key 应使用不可变对象，如 String、Integer。

### Q003 ★★★ 极高 String 为什么设计成不可变？

为了线程安全、可安全共享、哈希值可缓存、以及支撑字符串常量池；不可变让 String 可以像常量一样到处传递而无需拷贝。

- 实现手段：String 类 final，内部 char[]（JDK 9 起改为 byte[] + coder 压缩存储）也是 final 且不对外暴露。
- 线程安全：状态不可变，多线程读无竞态，天然的 immutable 对象。
- 哈希缓存：hash 字段第一次计算后缓存，使 String 成为 HashMap 最理想的 key。
- 常量池：字面量可以复用同一份实例，"a"+"b" 编译期即可折叠。
- 安全性：类加载、网络地址、数据库连接串等作为 String 传入后不会被中途篡改。

> **记忆点**：安全（线程/共享）+ 哈希可缓存 + 常量池复用 + 防篡改。

#### 追问：JDK 9 为什么把 char[] 换成 byte[]？

多数拉丁字符用 Latin-1 一字节就能表示，用 char[] 每个字符固定 2 字节是浪费。改成 byte[] + coder 标识编码后，纯英文/数字字符串内存直接减半，中文仍用 UTF-16 两字节，整体堆占用显著下降。

### Q004 ★★★ 极高 String、StringBuilder、StringBuffer 怎么选？

少量拼接或常量用 String；单线程大量拼接用 StringBuilder；多线程共享同一缓冲区才用 StringBuffer（方法加了 synchronized，有锁开销）。

| 类型 | 可变性 | 线程安全 | 性能 | 典型场景 |
| --- | --- | --- | --- | --- |
| String | 不可变 | 安全（因不可变） | 每次拼接产生新对象 | 常量、少量拼接、Map key |
| StringBuilder | 可变 | 不安全 | 最快 | 循环内拼接、SQL 拼装 |
| StringBuffer | 可变 | 安全（synchronized） | 中等 | 极少，老代码 |

- 为什么循环里 s += i 危险：每次生成新 String，JDK 8 编译成 StringBuilder + toString，JDK 9+ 用 invokedynamic 的 StringConcatFactory，但循环内仍是 O(n²) 对象分配。
- 容量预判：new StringBuilder(64) 能减少扩容拷贝，扩容是 (旧容量 \<\< 1) + 2。

> **记忆点**：不可变靠 String，单线程靠 Builder，多线程才 Buffer。

#### 追问："a" + "b" + "c" 编译期发生了什么？

常量折叠。javac 在编译期直接算成 "abc" 一个字面量放进常量池，运行时零拼接开销。只有含变量的拼接才会走 StringBuilder / invokedynamic。

### Q005 ★★★ 高 Java 8 / 17 / 21 各有哪些值得说的新特性？

8 是 Lambda/Stream/Optional/新日期 API/接口默认方法；17 是密封类、模式匹配 instanceof、record 转正、文本块、ZGC 转正；21 是虚拟线程、switch 模式匹配、record 模式、分代 ZGC、顺序集合。

- Java 8：最重要的分水岭。Stream 惰性求值 + 短路、Optional 治 NPE、LocalDate/LocalDateTime 替换 Date、CompletableFuture。
- Java 11：var（局部变量类型推断）、HttpClient、String.strip/isBlank。
- Java 17（LTS）：sealed interface 限制继承者；record 自动生成构造器/equals/hashCode/toString；instanceof 模式匹配省去强转；文本块 """。
- Java 21（LTS）：虚拟线程（Thread.ofVirtual()，由 JVM 调度到少量载体线程，阻塞时自动让出，极大提升 IO 密集型吞吐）；switch 模式匹配；分代 ZGC；SequencedCollection 统一首尾操作。
- 面试口径：说自己项目用 Java 21 并讲虚拟线程的适用边界（见并发篇）。

> **记忆点**：8 函数式，17 密封 + record，21 虚拟线程。

#### 追问：record 和 Lombok 的 @Data 有什么区别？

record 是语言级特性：final 类、字段全 final、自动生成全参构造与访问器（x() 而非 getX()）、equals/hashCode/toString，不支持继承其他类但可实现接口，可作 DTO / 返回值。Lombok 是编译期注解处理器，生成普通 Java 类，可继承、可变、有 setter，但是第三方依赖且会污染 IDE/构建。不可变场景优先 record。

## 二、集合框架

### Q006 ★★★ 极高 ArrayList 和 LinkedList 怎么选？

底层结构不同决定了性能：ArrayList 是动态数组，随机访问 O(1)、中间插入删除要挪元素；LinkedList 是双向链表，头尾操作 O(1)、随机访问 O(n)。实际开发默认用 ArrayList，几乎不用 LinkedList。

- ArrayList：Object[] elementData，内存连续，CPU 缓存友好，get(i) 直接下标寻址。
- LinkedList：Node{item, prev, next}，每个节点额外两个指针，内存不连续，缓存不友好。
- 插入删除的真相：LinkedList 虽然插入是 O(1)，但先要 O(n) 找到位置；而 ArrayList 的 add(e) 尾部追加均摊也是 O(1)。所以只有「用 ListIterator 在遍历中频繁增删」LinkedList 才有优势。
- 内存：LinkedList 每个元素多 24 字节左右的节点开销，1 万个元素多占约 240KB。
- 队列场景：需要 FIFO 用 ArrayDeque，比 LinkedList 更快（也是 JDK 推荐）。

> **记忆点**：查多用 Array，头尾增删用 ArrayDeque，LinkedList 基本只是面试题。

#### 追问：ArrayList 线程安全吗？怎么变成线程安全？

不安全，多线程 add 会丢数据或数组越界（ArrayIndexOutOfBoundsException）。三种做法：Collections.synchronizedList（全表加锁，读也锁）、CopyOnWriteArrayList（写时复制，读无锁，适合读多写少）、或外部自己加锁 / 用 java.util.concurrent 的队列。

### Q007 ★★★ 极高 ArrayList 的扩容机制？

默认初始容量 10（第一次 add 时才分配，无参构造是懒加载空数组），扩容为原容量的 1.5 倍（oldCapacity + (oldCapacity \>\> 1)），通过 Arrays.copyOf 拷贝到新数组。

- 触发点：size + 1 \> elementData.length 时调用 grow()。
- 1.5 倍是空间与拷贝次数的折中：太小频繁拷贝，太大浪费内存（对比 HashMap 的 2 倍，因为哈希表容量要求 2 的幂）。
- 均摊复杂度：追加 n 个元素总拷贝量约 2n，均摊 O(1)。
- 优化：已知大小时 new ArrayList\<\>(expectedSize) 避免多次扩容。
- 删除元素不会缩容（remove 只把后面元素前移、末尾置 null），需要缩容手动调 trimToSize()。

> **记忆点**：懒加载 10，扩容 1.5 倍，拷贝 Arrays.copyOf，删除不缩容。

#### 追问：ArrayList.remove() 在 for 循环里会有什么问题？

用 for (int i...) 正序删除会漏删（删除后后面元素前移，i 又自增跳过一个）。正确做法：倒序遍历删除、用 Iterator.remove()、或 removeIf。用增强 for 删除会抛 ConcurrentModificationException（fail-fast）。

### Q008 ★★★ 极高 HashMap 1.8 的底层结构是什么？

数组 + 链表 + 红黑树。Node[] table 数组，哈希冲突时挂链表，链表长度 ≥ 8 且数组容量 ≥ 64 时转为红黑树，树节点数 ≤ 6 时退化回链表。

- 数组：Node\<K,V\>[] table，长度始终是 2 的幂，默认 16。
- 链表：Node 带 hash、key、value、next。
- 红黑树：TreeNode，查找从 O(n) 降到 O(log n)，防止哈希碰撞攻击（大量 key 落同一桶导致退化）。
- 为什么阈值是 8：泊松分布下，链表长度到 8 的概率约 0.00000006，正常情况几乎不会树化，8 是「防恶意碰撞」与「树化开销」的平衡点。
- 为什么退化阈值是 6 而不是 7：留缓冲，避免在 7/8 之间反复树化与退化抖动。
- JDK 7 与 8 的差异：7 是「数组 + 链表」，头插法，扩容时可能形成环形链表导致 CPU 100%；8 改尾插法并加入红黑树。

> **记忆点**：数组 + 链表 + 红黑树；8 树化，6 退化，64 是前提。

#### 追问：为什么树化还要求数组容量 ≥ 64？

容量小的时候冲突主要来自「桶太少」而不是「哈希不好」，此时应该先扩容分散元素，而不是花代价建树。所以 treeifyBin 里若 table.length \< 64 会先 resize() 扩容。

### Q009 ★★★ 极高 HashMap 的 put 流程是怎样的？

① 算 key 的扰动哈希 (h = key.hashCode()) ^ (h \>\>\> 16)；② 数组为空先初始化；③ 定位桶 (n-1) & hash，桶空则直接放；④ 桶不空则比较哈希与 equals，相等就覆盖 value；⑤ 是树节点走红黑树插入；⑥ 否则遍历链表尾插，链长到 8 尝试树化；⑦ ++size \> threshold 则扩容。

- 索引计算用位运算 (n-1) & hash 而不是取模，因为 n 是 2 的幂时两者等价且位运算更快。
- 扰动函数把高 16 位异或到低 16 位，让高位也参与定位，减少碰撞。
- 覆盖判断：hash 相等且 (k = e.key) `==` key || key.equals(k)。
- 允许一个 null key，固定放在下标 0 的桶（hash(null) = 0）。
- 扩容后元素要么留在原位 i，要么移到 i + oldCap（因为容量翻倍，多了一个高位），这是 1.8 扩容高效的关键。

> **记忆点**：扰动 → 取模定桶 → 空放/覆盖/树插/尾插 → 超阈值扩容。

#### 追问：HashMap 的 key 为什么推荐用 String / Integer？

因为它们不可变且 hashCode 已实现良好，String 还缓存了哈希值。用自定义对象作 key 必须重写 equals 和 hashCode，且保证对象入表后参与哈希的字段不再变化。

### Q010 ★★★ 高 HashMap 的扩容机制？为什么容量必须是 2 的幂？

负载因子 0.75，元素数超过 容量 × 0.75 就扩容为原容量 2 倍，然后把旧数组元素重新分布到新数组。容量取 2 的幂是为了用 (n-1) & hash 代替取模，并且保证扩容后元素只可能落在「原位」或「原位 + 旧容量」两个位置。

- 阈值：threshold = capacity \* loadFactor，默认 16 × 0.75 = 12，第 13 个元素触发扩容。
- 负载因子 0.75 的折中：太小浪费空间，太大冲突变多、查询变慢，0.75 在空间与时间上较平衡（也是泊松分布下较优的值）。
- 1.8 的扩容优化：不再重新计算哈希，而是看 hash & oldCap 是否为 0，把链表拆成「低位链」和「高位链」两条，分别挂到 j 和 j + oldCap，避免逐个 rehash。
- 若构造时指定了容量，tableSizeFor 会向上取到最近的 2 的幂（如传 10 得到 16）。
- 扩容是 O(n) 操作，频繁扩容很伤性能，预估容量时建议 (expectedSize / 0.75) + 1。

> **记忆点**：0.75 触发，翻倍扩容，位运算判高低位，容量 2 的幂。

#### 追问：HashMap 初始容量传 1000 会怎样？

构造时 tableSizeFor(1000) 得到 1024；而阈值在第一次 put 时才按 1024 \* 0.75 = 768 计算。注意 new HashMap(1000) 只是设了阈值参数，数组仍然是懒加载的。

### Q011 ★★★ 极高 HashMap 为什么线程不安全？会发生什么？

因为它没有任何同步措施，多线程并发 put 时会出现数据覆盖、size 计算错误、扩容期间读到 null 或死循环（JDK 7）。并发场景必须用 ConcurrentHashMap。

- JDK 7 的头插法 + 并发扩容会形成环形链表，之后 get 死循环，CPU 打满。
- JDK 8 改尾插法后不再有环形链表，但仍会丢数据：两个线程同时往同一个空桶写，后写的覆盖先写的。
- size 是普通 int 自增，非原子，并发下计数不准。
- 扩容时 table 引用替换与元素迁移不是原子的，其他线程可能读到半迁移状态。
- 快速失败：并发修改会让迭代器抛 ConcurrentModificationException（modCount 校验）。

> **记忆点**：7 死循环，8 丢数据，size 不准；并发就用 ConcurrentHashMap。

#### 追问：Collections.synchronizedMap 和 ConcurrentHashMap 有什么区别？

前者是给整个 Map 包一层 synchronized，所有读写串行，粒度是「整张表」，并发度约等于 1；后者锁粒度细化到桶（1.8 是 CAS + 单个桶头节点 synchronized），读操作基本无锁（volatile 读），并发度高得多。前者还要求手动同步遍历。

### Q012 ★★★ 极高 ConcurrentHashMap 1.8 是怎么实现线程安全的？

用 CAS + synchronized：table 数组用 volatile 保证可见性；桶为空时用 CAS 写入（无锁）；桶非空时只对该桶的头节点加 synchronized，锁粒度细到单个桶；size 用 baseCount + CounterCell[] 分段累加。

- 与 1.7 的差别：1.7 是 Segment 分段锁（默认 16 段，锁的是段），1.8 去掉了 Segment，锁粒度更细，并且引入红黑树。
- 读操作：get 不加锁，靠 volatile 读 table 与 Node.val 保证可见。
- 写操作：put 先 CAS 抢占空桶；非空则 synchronized (f) 锁桶首节点，再按链表/红黑树插入。
- 扩容：支持多线程协助扩容（ForwardingNode 标记已迁移的桶，helpTransfer），迁移时每个线程领一段。
- 弱一致性迭代器：遍历时不抛 ConcurrentModificationException，但不保证看到最新数据。
- 不允许 null key / null value（无法区分「不存在」和「值为 null」，且并发下会歧义）。

> **记忆点**：空桶 CAS，非空锁桶头，size 用 CounterCell，扩容可协作。

#### 追问：为什么 ConcurrentHashMap 不允许 null？

并发场景下，get 返回 null 无法判断是「key 不存在」还是「value 就是 null」，而 containsKey 与 get 之间存在竞态，无法像 HashMap 那样二次确认。为了避免这种歧义，直接禁止 null。

## 三、并发编程

### Q013 ★★★ 极高 线程池的核心参数有哪些？

ThreadPoolExecutor 七个参数：核心线程数 corePoolSize、最大线程数 maximumPoolSize、空闲存活时间 keepAliveTime + 时间单位、任务队列 workQueue、线程工厂 threadFactory、拒绝策略 handler。

- corePoolSize：常驻线程数，即使空闲也不回收（除非 allowCoreThreadTimeOut(true)）。
- maximumPoolSize：线程数上限，只有在队列满了之后才扩到这么多。
- keepAliveTime：超过核心数的线程空闲多久被回收。
- workQueue：ArrayBlockingQueue（有界，推荐）、LinkedBlockingQueue（默认无界，危险）、SynchronousQueue（不存元素，直接交给线程）、PriorityBlockingQueue、DelayQueue。
- threadFactory：自定义线程名，强烈建议，方便排查（如 zxq-async-%d）。
- handler：拒绝策略，见后题。

> **记忆点**：核心数、最大数、存活时间、队列、工厂、拒绝策略——七参数；队列满了才扩线程。

#### 追问：Executors 提供的四种线程池为什么不建议用？

newFixedThreadPool 和 newSingleThreadExecutor 用无界 LinkedBlockingQueue，任务堆积会 OOM；newCachedThreadPool 和 newScheduledThreadPool 的 maximumPoolSize 是 Integer.MAX_VALUE，线程数可能无限增长导致 OOM。阿里规约明确要求手动 new ThreadPoolExecutor 并指定有界队列。

### Q014 ★★★ 极高 线程池的任务提交与执行流程是怎样的？

提交任务后：① 当前线程数 \< 核心数 → 新建核心线程执行；② 否则尝试入队；③ 入队成功则等空闲线程取；④ 入队失败（队列满）且线程数 \< 最大数 → 新建非核心线程；⑤ 还不行就执行拒绝策略。

- 顺序口诀：核心线程 → 队列 → 扩容到最大 → 拒绝。
- 关键坑：用无界队列时，步骤 ④⑤ 永远不会触发，maximumPoolSize 形同虚设（FixedThreadPool 就是这样）。
- 空闲线程的获取：核心线程用 poll() 阻塞等待，非核心线程用带超时的 poll(keepAliveTime)，超时就回收。
- 线程复用：Worker 内部循环 getTask() 取任务，取到就执行，取不到（返回 null）就退出，这就是「线程池不销毁线程」的原因。

> **记忆点**：先核心，再排队，排不下才扩，扩不下就拒。

#### 追问：线程池里的线程执行完任务为什么不会死？

ThreadPoolExecutor 把线程包装成 Worker extends AQS，runWorker 方法里是一个 while (task != null || (task = getTask()) != null) 的循环，执行完任务后回到 getTask() 阻塞在队列的 poll/take 上继续等下一个任务，直到 getTask() 返回 null（超时或线程池关闭）才退出。

### Q015 ★★★ 高 线程池的核心线程数怎么设置？

经验公式：CPU 密集型 = CPU 核数 + 1（+1 用于应对偶发缺页中断），IO 密集型 = CPU 核数 × (1 + 平均等待时间 / 平均计算时间)，实际要以压测为准，并配合监控动态调。

- 纯计算任务（加解密、复杂算法）：线程多了只会增加上下文切换，N+1 即可。
- IO 等待任务（DB、HTTP、文件）：线程大部分时间在等，可以显著大于核数，2N ~ 4N 都常见。
- 更准确的口径：N × (1 + W/C)，其中 W 是等待时间、C 是计算时间。如果等待占比 90%，理论上是 10N。
- 工程约束：还要受下游承载能力限制（DB 连接池、对方接口 QPS），线程池再大也只会把下游打挂。
- 最佳实践：核心与最大设成一样（避免反复创建销毁），队列容量按可接受延迟给，并开 allowCoreThreadTimeOut 处理突发。

> **记忆点**：CPU 密集 N+1，IO 密集 N×(1+W/C)，最终靠压测定。

#### 追问：corePoolSize `==` maximumPoolSize 有什么好处？

线程池规模稳定，不会因为流量突增而临时扩容、突降后又销毁，避免线程频繁创建销毁的开销，也避免线程数抖动带来的延迟毛刺。配合有界队列 + 合理拒绝策略，过载时直接快速失败（fail-fast），行为可预测。

### Q016 ★★★ 极高 synchronized 的原理是什么？锁升级过程是怎样的？

synchronized 编译后生成 monitorenter / monitorexit 指令，JVM 通过对象头 Mark Word + Monitor（管程） 实现。为了减少重量级锁的系统调用开销，JDK 6 起引入锁升级：无锁 → 偏向锁 → 轻量级锁（CAS 自旋）→ 重量级锁（OS 互斥量），只能升不能降。

- 修饰实例方法：锁 this；修饰静态方法：锁 Class 对象；修饰代码块：锁指定对象。
- 偏向锁：只有一个线程访问时，把线程 ID 记在 Mark Word，后续进入无需 CAS（JDK 15 起默认禁用，JDK 18 移除，因为撤销代价高、现代应用几乎都有竞争）。
- 轻量级锁：多线程交替执行时，线程在栈帧里建 Lock Record，用 CAS 把 Mark Word 指向它，失败则自旋。
- 重量级锁：自旋失败后膨胀为 ObjectMonitor，未获取到锁的线程进入 EntryList 阻塞，涉及内核态切换。
- 可重入：Monitor 内有 owner 和 recursions（重入计数），同一线程再次进入只加计数。

> **记忆点**：monitorenter/exit + Mark Word + Monitor；升级链：偏向 → 轻量 → 重量，只升不降。

#### 追问：偏向锁为什么被废弃？

偏向锁的收益只在「几乎无竞争」的场景，但一旦出现竞争就要 safepoint 撤销，撤销成本很高；而且现代应用多是高并发、短临界区，偏向锁反而拖累吞吐。JDK 15 默认关闭（-XX:-UseBiasedLocking），JDK 18 彻底移除。

### Q017 ★★★ 极高 volatile 的作用和原理？

两件事：保证可见性、禁止指令重排序；但不保证原子性。实现上靠内存屏障（LoadLoad/StoreStore/LoadStore/StoreLoad），写 volatile 时插入 StoreStore + StoreLoad 屏障，把工作内存刷回主存并让其他 CPU 缓存行失效（MESI）。

- 可见性：读 volatile 变量强制从主存读，写强制刷主存，绕过 CPU 缓存不一致。
- 有序性：禁止 volatile 写与之前的读写重排、禁止 volatile 读与之后的读写重排，即 happens-before 的传递链。
- 经典用途 1：状态标志位 volatile boolean running，一个线程改、另一个线程立刻看到。
- 经典用途 2：DCL 单例的 instance 必须 volatile，否则 new 的三步（分配内存、初始化、赋引用）可能重排，另一线程拿到未初始化完的对象。
- 不保证原子：i++ 是「读-改-写」三步，volatile 挡不住并发丢失更新，要用 AtomicInteger。

> **记忆点**：volatile = 可见 + 有序，不原子；DCL 单例不加它就出 bug。

#### 追问：i++ 用 volatile 修饰能保证线程安全吗？

不能。i++ 编译成 getfield → iadd → putfield 三条指令，volatile 只保证每一步的可见性，不保证三步的原子性，两个线程可能同时读到 i=1 都写回 2。解决：AtomicInteger.incrementAndGet()（CAS）或 synchronized。

### Q018 ★★★ 高 JMM 是什么？happens-before 有哪些规则？

JMM（Java 内存模型）是规范，定义了线程与主内存的交互规则：每个线程有自己的工作内存（抽象概念，对应 CPU 缓存 + 寄存器），共享变量存主存，线程间通信必须经过主存；happens-before 是判断「是否可见、是否可重排」的规则集。

- 程序顺序规则：同一线程内，前面的操作 happens-before 后面的操作。
- 监视器锁规则：解锁 happens-before 后续对同一锁的加锁。
- volatile 规则：对 volatile 变量的写 happens-before 后续对该变量的读。
- 线程启动规则：Thread.start() happens-before 新线程中的任何操作。
- 线程终止规则：线程中所有操作 happens-before 其他线程检测到它终止（join 返回）。
- 传递性：A hb B，B hb C ⇒ A hb C。

> **记忆点**：程序顺序、锁、volatile、start、join、传递——六条够用。

#### 追问：JMM 里的「工作内存」是真实存在的内存吗？

不是，它是抽象模型，落地到硬件就是 CPU 的寄存器、L1/L2 缓存和写缓冲区。JMM 的作用是屏蔽不同 CPU 架构的差异，让「可见性、有序性、原子性」的语义在 Java 层面统一，具体靠内存屏障指令实现。

### Q019 ★★★ 极高 CAS 是什么？ABA 问题怎么解决？

CAS（Compare And Swap）是「比较并交换」的原子指令，三个操作数：内存值 V、期望值 A、新值 B，只有 V `==` A 时才把 V 改成 B，否则失败重试。底层是 Unsafe.compareAndSwapInt → CPU 的 cmpxchg 指令 + lock 前缀保证原子。ABA 问题指值从 A 改成 B 又改回 A，CAS 察觉不到变化。

- 优点：无锁、无阻塞、无上下文切换，适合竞争不激烈的计数场景。
- 缺点 1：ABA。解决：加版本号，用 AtomicStampedReference / AtomicMarkableReference。
- 缺点 2：自旋消耗 CPU，竞争激烈时不如锁。
- 缺点 3：只能保证一个变量的原子性，多变量要么用 AtomicReference 打包，要么加锁。
- 典型应用：AtomicInteger、ConcurrentHashMap 的空桶写入、AQS 里 state 的修改。

> **记忆点**：CAS = V`==`A ? B : 失败；ABA 用版本号；自旋耗 CPU。

#### 追问：AtomicInteger 和 synchronized 加锁哪个快？

低竞争时 AtomicInteger 快（用户态 CAS，无内核切换）；高竞争时 CAS 疯狂失败重试，反而不如 synchronized（有锁升级与排队机制）。所以高并发计数推荐 LongAdder（分散热点）。

### Q020 ★★★ 高 AQS 是什么？ReentrantLock 怎么基于它实现？

AQS（AbstractQueuedSynchronizer）是一个用 volatile int state + CLH 双向队列 实现的同步器框架：state 表示同步状态，获取失败的线程包装成 Node 排队，靠 LockSupport.park/unpark 阻塞与唤醒。ReentrantLock 用 state 表示重入次数（0 表示空闲，N 表示被重入 N 次）。

- 独占模式：tryAcquire CAS 把 state 从 0 改成 1，失败则入队 park；释放时 state--，减到 0 再唤醒队首。
- 共享模式：tryAcquireShared，state 表示剩余许可数（Semaphore、CountDownLatch 用它）。
- 重入：state 递增，exclusiveOwnerThread 记录持有者，释放时递减到 0 才真正释放。
- 公平锁：hasQueuedPredecessors() 判断队里有没有更早的等待者；非公平锁直接 CAS 抢，抢不到再排队（性能更高，但可能饥饿）。
- 模板方法：子类只需实现 tryAcquire / tryRelease，排队、阻塞、唤醒由 AQS 完成。

> **记忆点**：AQS = volatile state + CLH 队列 + park/unpark；state 含义由子类定义。

#### 追问：ReentrantLock 的公平锁和非公平锁怎么选？

默认非公平。非公平锁允许「插队」直接 CAS，减少了线程唤醒的上下文切换开销，吞吐通常更高（实测可高出数倍）；公平锁严格 FIFO，避免饥饿，但每次都要检查队列，性能较低。只有在「必须保证请求顺序」的场景（如某些任务调度）才用公平锁。

### Q021 ★★★ 极高 ThreadLocal 的原理？为什么会内存泄漏？

每个 Thread 内部有一个 ThreadLocalMap（key 是 ThreadLocal 的弱引用，value 是强引用），get/set 实际是操作当前线程自己的 map，从而实现线程隔离。内存泄漏的根因是 key 被回收后 value 还挂在 Entry 上，而 Entry 又随线程对象存活。

- 结构：Thread → ThreadLocalMap → Entry[] (WeakReference\<ThreadLocal\>, value)。
- 为什么 key 用弱引用：当 ThreadLocal 对象不再被外部引用，可以被 GC 回收，避免 key 泄漏。
- 泄漏链：key 被 GC 后变成 null，但 value 是强引用且 Entry 挂在线程的 map 上；若线程池里的核心线程长期存活，value 就一直回收不掉。
- 兜底机制：get/set/remove 时如果检测到 key 为 null 的 Entry 会顺手清理（探测式清理），但不保证及时。
- 正确用法：用完必须 remove()，尤其在线程池里；try/finally 包起来。

> **记忆点**：key 弱、value 强；线程活着 value 就活着；用完 remove。

#### 追问：ThreadLocal 在父子线程间怎么传递？

默认不能传递（子线程有自己独立的 ThreadLocalMap）。用 InheritableThreadLocal 在 new Thread() 时把父线程的 map 浅拷贝过去，但线程池场景失效（线程是复用的，不会重新创建）。线程池场景要用阿里的 TransmittableThreadLocal（TTL），在任务提交时把上下文快照包进任务里。

### Q022 ★★★ 高 CompletableFuture 的常用方法和线程池怎么指定？

用 supplyAsync / runAsync 提交异步任务，thenApply / thenCompose / thenCombine 做串行与并行编排，allOf 等全部完成、anyOf 等任一完成，exceptionally / handle 处理异常。默认用 ForkJoinPool.commonPool()，IO 任务必须传自定义线程池。

- thenApply 是同步转换（同线程执行或由完成线程执行），thenApplyAsync 会切到线程池。
- thenCompose 用于嵌套 CompletableFuture（扁平化），类似 flatMap；thenCombine 合并两个独立结果。
- allOf 返回 CompletableFuture\<Void\>，要拿各任务结果得自己遍历 join()。
- 异常：exceptionally 只处理异常并给兜底值；handle 无论成功失败都执行；whenComplete 不改变结果。
- 默认池的坑：commonPool 并行度 = CPU 核数 - 1，IO 阻塞会拖垮全局，必须传业务线程池。

```java
ExecutorService pool = new ThreadPoolExecutor(8, 8, 60, TimeUnit.SECONDS,
        new ArrayBlockingQueue<>(200), new ThreadFactoryBuilder().setNameFormat("zip-%d").build(),
        new ThreadPoolExecutor.CallerRunsPolicy());

CompletableFuture<String> fetch = CompletableFuture.supplyAsync(() -> oss.download(url), pool);
CompletableFuture<byte[]> zip  = fetch.thenApplyAsync(this::zip, pool);
CompletableFuture<String> up   = zip.thenComposeAsync(this::upload, pool)
        .exceptionally(e -> { log.error("zip-upload failed", e); return null; });
```

> **记忆点**：supplyAsync 起任务，then\* 编排，allOf 聚合，IO 必须传自定义池。

#### 追问：CompletableFuture 的 join() 和 get() 有什么区别？

join() 抛非受检的 CompletionException，不需要 try-catch；get() 抛受检的 InterruptedException / ExecutionException，必须处理。功能上等价，代码里聚合多个 future 时用 join() 更简洁。

### Q023 ★★★ 高 虚拟线程是什么？它解决了什么问题？

虚拟线程（JDK 21 正式）是 JVM 管理的轻量级线程，由少量「载体线程（ForkJoinPool）」调度。它在阻塞时自动让出载体线程，所以能用同步阻塞的写法获得接近异步的吞吐，把「一个请求一个线程」的模型重新变得可行。

- 成本：创建约几百字节到几 KB，可以开百万级；平台线程受限于 OS，几千个就吃紧。
- 适用：IO 密集型（HTTP 调用、DB 查询、文件读写），代码保持简单同步风格。
- 不适用：CPU 密集型任务，用虚拟线程不会更快，反而多一层调度开销。
- 关键限制 pinning：在 synchronized 块内阻塞、或调用 native 方法时会钉住载体线程，无法让出（JDK 24 起 synchronized 的 pinning 已大幅缓解，但容器里仍需注意）。
- 另一个坑：ThreadLocal 仍可用但数量大时内存放大；CPU 密集与 IO 混合时要配信号量限流（虚拟线程本身不是限流器）。

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 10_000).forEach(i ->
        executor.submit(() -> { Thread.sleep(Duration.ofMillis(10)); return i; }));
}
```

> **记忆点**：虚拟线程 = 阻塞即让出，吃 IO 不吃 CPU；小心 pinning 和无限流。

#### 追问：用了虚拟线程还需要线程池吗？

不需要「池化」——虚拟线程创建极廉价，不要复用，用 newVirtualThreadPerTaskExecutor 每任务一个。但仍需要并发限流（Semaphore）保护下游资源，否则 10 万虚拟线程同时打 DB 一样会把数据库打挂。

## 四、JVM

### Q024 ★★★ 极高 JVM 运行时数据区有哪些？哪些线程私有？

五个区：方法区（元空间）、堆 是线程共享；虚拟机栈、本地方法栈、程序计数器 是线程私有。堆是 GC 主战场，方法区存类元信息。

- 程序计数器（PC）：记录当前线程执行到哪条字节码，唯一不会 OOM 的区域；用于线程切换后恢复执行位置。
- 虚拟机栈：每个方法调用创建一个栈帧（局部变量表、操作数栈、动态链接、方法出口）。-Xss 控制大小，递归过深抛 StackOverflowError。
- 本地方法栈：为 native 方法服务。
- 堆：对象实例和数组，分新生代（Eden + Survivor×2）和老年代，-Xms/-Xmx 控制。
- 方法区：JDK 8 起用元空间（Metaspace） 实现，位于本地内存，默认不限制（-XX:MaxMetaspaceSize 可设）。JDK 7 及以前是永久代（-XX:MaxPermSize），这也是 String.intern() 从永久代移到堆的原因。

> **记忆点**：共享堆和方法区，私有 PC、虚拟机栈、本地方法栈；元空间在堆外。

#### 追问：JDK 8 为什么用元空间替换永久代？

永久代受 JVM 堆大小限制且大小难调，容易 PermGen space OOM；元空间使用本地内存，上限受物理内存约束，且由 MetaspaceSize 动态调整，同时字符串常量池、静态变量迁到堆，减少了永久代的压力。

### Q025 ★★★ 极高 怎么判断一个对象可以被回收？GC Roots 有哪些？

用可达性分析：从 GC Roots 出发遍历引用链，不可达的对象才可回收。GC Roots 包括：虚拟机栈中局部变量引用的对象、方法区静态属性引用的对象、常量引用的对象、本地方法栈中 JNI 引用的对象、活跃线程、同步锁持有的对象等。

- 为什么不只用引用计数：无法解决循环引用（A 引用 B，B 引用 A，计数都不为 0 但实际不可达），而且计数增减有性能开销。
- 即使不可达也不一定立刻回收：要经过两次标记，若对象重写了 finalize() 且未被调用过，会被放进 F-Queue 并给一次「自救」机会（现已废弃）。
- 引用类型：强引用（不回收）、软引用（内存不足时回收，适合缓存）、弱引用（下次 GC 必回收，ThreadLocalMap 的 key）、虚引用（回收时收到通知，管理直接内存）。

> **记忆点**：可达性分析看 GC Roots；栈、静态、常量、JNI、活跃线程是根。

#### 追问：为什么 ThreadLocalMap 的 key 用弱引用，而 HashMap 的 key 用强引用？

ThreadLocalMap 的 key 弱引用是为了让无外部引用的 ThreadLocal 对象能被回收，避免 key 泄漏（value 侧泄漏靠 remove 兜底）。普通 HashMap 是业务数据结构，key 必须强引用，否则用着用着 key 就没了。

### Q026 ★★★ 极高 垃圾回收算法有哪几种？各自的优缺点？

三种基础算法：标记-清除（有碎片、效率一般）、复制（无碎片、但浪费一半空间、适合存活率低的新生代）、标记-整理（无碎片、但移动对象成本高、适合老年代）。分代收集就是把它们按代套用。

| 算法 | 过程 | 优点 | 缺点 | 用在哪 |
| --- | --- | --- | --- | --- |
| 标记-清除 | 标记存活 → 清除垃圾 | 实现简单、不移动对象 | 产生内存碎片、标记与清除效率低 | CMS |
| 复制 | 存活对象复制到另一半 | 无碎片、分配快（指针碰撞） | 浪费空间、存活多时复制成本高 | 新生代（Eden + Survivor） |
| 标记-整理 | 标记存活 → 向一端移动 → 清理边界 | 无碎片 | 移动对象需更新引用，停顿长 | 老年代（Serial Old、Parallel Old） |

- 分代假说：绝大多数对象朝生夕死（弱分代假说），所以新生代用复制算法最划算。
- 新生代比例默认 Eden : S0 : S1 = 8 : 1 : 1（-XX:SurvivorRatio=8），只浪费 10%。
- 为什么需要两个 Survivor：复制算法需要一个空的接收区，两个 Survivor 轮换，保证 Eden 每次都能用满。

> **记忆点**：新生代复制，老年代标记整理/清除；8:1:1 双 Survivor 轮换。

#### 追问：对象什么时候进入老年代？

三条路径：① 年龄达到 -XX:MaxTenuringThreshold（默认 15），每熬过一次 Minor GC 年龄 +1；② 动态年龄判定：Survivor 中同年龄对象总大小超过 Survivor 的一半，则大于等于该年龄的直接晋升；③ 大对象直接进老年代（-XX:PretenureSizeThreshold），避免在 Eden/Survivor 间反复复制。

### Q027 ★★★ 极高 常见的垃圾收集器有哪些？怎么选？

分三代：Serial / ParNew / Parallel Scavenge（新生代，分代模型）、CMS（并发标记清除，已废弃）、G1（JDK 9 起默认，可预测停顿）、ZGC / Shenandoah（低延迟，ZGC 停顿 \< 1ms）。实习面试只要说清 G1 是默认、ZGC 是低延迟，再讲清各自的并发/并行属性即可。

- Serial：单线程，Stop-The-World，客户端模式或小内存场景。
- Parallel Scavenge / Parallel Old：多线程、吞吐优先，JDK 8 的默认组合，适合批处理。
- CMS：并发标记清除，追求低停顿，但用标记-清除有碎片、有 Concurrent Mode Failure、且 JDK 9 废弃、JDK 14 移除。现在不要再答「线上用 CMS」。
- G1：把堆切成大小相等的 Region（1–32MB），按「回收收益」优先回收（Garbage First），用 -XX:MaxGCPauseMillis 设目标停顿，逻辑上仍分新生代/老年代但物理不连续。
- ZGC：染色指针 + 读屏障，并发标记与并发转移，JDK 15 转正，JDK 21 支持分代 ZGC，停顿通常在亚毫秒级，适合大堆低延迟（几十 GB～TB）。

> **记忆点**：JDK 8 默认 Parallel，JDK 9+ 默认 G1，超低延迟用 ZGC；CMS 已死。

#### 追问：G1 相比 CMS 的核心改进是什么？

① CMS 是整堆标记-清除，G1 是 Region 化 + 标记-整理（Region 内复制），不会产生严重碎片；② G1 能建立可预测的停顿模型（按 Region 回收收益排序，只回收一部分），CMS 无法控制停顿；③ G1 有 Remembered Set 处理跨 Region 引用，避免全堆扫描；④ G1 不会出现 CMS 的 Concurrent Mode Failure 退化成长停顿。

### Q028 ★★★ 极高 类加载的过程是怎样的？什么是双亲委派？

加载 → 验证 → 准备 → 解析 → 初始化。双亲委派：类加载器收到请求先委派给父加载器，父加载器无法完成才自己加载，保证核心类库不被篡改、类只被加载一次。

- 加载：通过全限定名获取二进制字节流，生成 Class 对象。
- 验证：文件格式、元数据、字节码、符号引用验证，防止恶意字节码。
- 准备：为静态变量分配内存并赋零值（static int a = 10 此时 a = 0，赋 10 在初始化阶段）。
- 解析：把常量池的符号引用替换为直接引用（可延迟到首次使用时）。
- 初始化：执行 \<clinit\>，即静态变量赋值与静态代码块，父类先于子类。
- 类加载器层级：Bootstrap（加载 java.\*，C++ 实现）→ Extension/Platform → Application → 自定义。
- 双亲委派的价值：java.lang.String 无论谁加载，最终都是 Bootstrap 加载的那份，防止自定义同名类替换核心类。

> **记忆点**：加载验证准备解析初始化；准备赋零值，初始化才赋真值；双亲委派防篡改防重复。

#### 追问：怎么打破双亲委派？举两个真实例子。

重写 ClassLoader.loadClass()（不是 findClass）即可绕过。① Tomcat：为每个 WebApp 建独立 WebappClassLoader，先自己加载应用类（实现应用隔离），核心类仍委派给 Bootstrap；② JDBC SPI：DriverManager 由 Bootstrap 加载，但它要加载厂商的 Driver 实现（在 classpath 上），Bootstrap 看不到，于是引入线程上下文类加载器（TCCL）反向委派；③ OSGi 的网状委派也是。

### Q029 ★★★ 高 常见 OOM 有哪些？线上怎么定位？

常见 Java heap space（堆溢出，对象太多/泄漏）、Metaspace（元空间溢出，动态生成类太多）、GC overhead limit exceeded（GC 占时超 98% 且回收不到 2%）、unable to create new native thread（线程数超系统限制）、Direct buffer memory（堆外内存）。定位靠 堆转储 + MAT 分析。

- 第一步：保留现场。-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/logs/，OOM 时自动 dump。
- 第二步：jmap -dump:format=b,file=heap.hprof \<pid\> 手动导出，jmap -histo:live \<pid\> | head -20 看对象直方图。
- 第三步：MAT / JProfiler 打开 hprof，看 Dominator Tree 找占用最大的对象，用 Path to GC Roots 排除弱引用/软引用后找到意外的强引用链。
- 高频成因：静态集合无限增长（本地缓存没设上限）、ThreadLocal 没 remove、监听器未注销、大 SQL 一次查全表、String 拼接、循环里创建大对象。
- 元空间 OOM：常见于 CGLIB 动态代理类暴涨、Groovy/脚本引擎、热部署。

> **记忆点**：堆溢出看 MAT 找 GC Roots 引用链；元空间看类加载数量；线程溢出看 ulimit。

#### 追问：内存泄漏和内存溢出有什么区别？

内存溢出（OOM）是结果：内存不够用了。内存泄漏是原因之一：对象该回收却回收不掉，逐渐累积最终 OOM。另一种 OOM 是「瞬时大对象」——不是泄漏，而是单次申请超过堆上限（如一次查了 100 万行）。定位时先看是「持续增长」还是「尖峰」，前者查泄漏，后者查业务代码。

### Q030 ★★★ 高 JVM 调优常用命令和工具？

jps 看进程、jstat -gcutil 看 GC 频率与各代占用、jmap 导堆和对象直方图、jstack 看线程栈查死锁/CPU 飙高、jcmd 是新一代统一入口、Arthas 是线上排查神器（dashboard/thread/trace/watch）。

- jstat -gcutil \<pid\> 1000 10：每秒一次，看 YGC/FGC 次数、GCT 总耗时、O（老年代使用率）。
- CPU 100% 排查链路：top -Hp \<pid\> 找最耗 CPU 的线程 → printf '%x' \<tid\> 转 16 进制 → jstack \<pid\> | grep -A 20 nid=0x\<hex\> 看栈。
- jstack 也能看线程数是否异常、有没有 BLOCKED、有没有死锁。
- Arthas 的 trace ClassName methodName 能看到方法内部每个调用的耗时，定位慢接口非常高效；watch 可以看方法入参出参。
- 线上不要轻易用 jmap -dump（会 STW 很久），优先 jcmd GC.heap_dump 或低版本用 -XX:+HeapDumpOnOutOfMemoryError 自动留。

> **记忆点**：jps 找进程，jstat 看 GC，jmap 看对象，jstack 看线程，Arthas 看链路。

#### 追问：线上 CPU 飙高怎么排查？说清楚完整步骤。

① top 找到高 CPU 的 Java 进程 PID；② top -Hp \<pid\> 找到最耗 CPU 的线程 TID；③ printf '%x\n' \<TID\> 转十六进制；④ jstack \<pid\> \> stack.log，用 nid=0x\<hex\> 搜索该线程的栈；⑤ 看栈顶是业务代码（死循环、正则回溯、频繁 GC）还是 GC 线程（GCTaskThread 说明是 GC 压力，需查内存）。⑥ 若线程频繁变化，用 jstack 连续采 3 次对比，或直接用 Arthas thread -n 3 看最忙的线程。

## 五、Spring 与 Spring Boot

### Q031 ★★★ 极高 Spring Bean 的生命周期？

实例化 → 属性填充 → Aware 回调 → BeanPostProcessor.postProcessBeforeInitialization → @PostConstruct → InitializingBean.afterPropertiesSet → init-method → postProcessAfterInitialization（AOP 代理在这里生成）→ 使用 → @PreDestroy → DisposableBean.destroy → destroy-method。

- 四步主干：实例化 → 属性赋值 → 初始化 → 销毁。
- 关键扩展点：BeanPostProcessor（对所有 Bean 生效，AOP 靠它生成代理）、BeanFactoryPostProcessor（在 Bean 实例化前修改 BeanDefinition，如 PropertySourcesPlaceholderConfigurer 解析占位符）。
- Aware 接口：BeanNameAware、BeanFactoryAware、ApplicationContextAware，用于拿到容器自身。
- 单例 Bean 在容器启动时创建（ApplicationContext 默认），原型 Bean 每次 getBean 都走完整流程。
- 销毁只在单例上生效；原型 Bean 的销毁容器不管。

> **记忆点**：实例化 → 填充 → 初始化（三回调）→ 使用 → 销毁（两回调）；AOP 在初始化后置处理生成。

#### 追问：@PostConstruct、afterPropertiesSet、init-method 三个的执行顺序？

@PostConstruct（JSR-250，由 CommonAnnotationBeanPostProcessor 调）→ InitializingBean.afterPropertiesSet() → XML/@Bean(initMethod) 指定的 init-method。销毁顺序对称：@PreDestroy → DisposableBean.destroy() → destroy-method。三者功能重叠，现代代码多用 @PostConstruct。

### Q032 ★★★ 极高 Spring 如何解决循环依赖？三级缓存分别是什么？

用三级缓存：singletonObjects（一级，成品 Bean）、earlySingletonObjects（二级，提前暴露的原始 Bean 或代理）、singletonFactories（三级，ObjectFactory 工厂）。A 依赖 B、B 依赖 A 时，A 实例化后先把工厂放进三级缓存，B 需要 A 时从三级缓存拿到（必要时提前生成 AOP 代理）并升级到二级缓存，从而打破循环。

- 为什么需要三级而不是两级：如果 A 需要 AOP 代理，B 拿到的必须是代理对象而不是原始对象。三级缓存的 ObjectFactory 提供了「延迟决定是否生成代理」的能力：只有在真的发生循环依赖时才提前调 getEarlyBeanReference 生成代理。
- 只支持 singleton + setter/字段注入；构造器注入的循环依赖无法解决（对象都造不出来，更谈不上提前暴露）。
- prototype 作用域的循环依赖也不支持，直接抛 BeanCurrentlyInCreationException。
- Spring Boot 2.6+ 默认禁止循环依赖（spring.main.allow-circular-references=false），这是官方在推「别写循环依赖」。
- 正确做法：重构，抽出公共依赖到第三个 Bean，或用 @Lazy 延迟注入。

> **记忆点**：一级成品、二级半成品、三级工厂；三级是为了 AOP 代理能延迟生成。

#### 追问：为什么官方从 2.6 开始默认禁止循环依赖？

循环依赖本质是设计问题——两个 Bean 互相依赖说明职责边界不清。而且三级缓存方案只覆盖 setter 注入的单例场景，构造器注入、prototype、@Async 代理等场景都会失效，容易在重构后突然报错。官方选择「启动即失败」，让问题在设计阶段暴露。

### Q033 ★★★ 极高 Spring AOP 的原理？JDK 动态代理和 CGLIB 怎么选？

AOP 基于动态代理：目标类实现了接口时默认用 JDK 动态代理（Proxy + InvocationHandler，生成实现同接口的代理类），没有接口时用 CGLIB（生成子类，字节码增强）。Spring Boot 2.x 起默认 proxyTargetClass=true，即统一用 CGLIB。

- JDK 代理限制：只能代理接口方法，代理对象与目标对象不是同一类型（不能强转成实现类）。
- CGLIB 限制：不能代理 final 类/final 方法，因为要继承并重写。
- 通知类型：@Before、@After、@AfterReturning、@AfterThrowing、@Around（最强大，可控制是否执行目标方法）。
- 织入时机：运行期织入（Spring AOP），不是编译期（AspectJ）。AspectJ 用 ajc 编译期/加载期织入，能力更强（可织入字段访问、构造器）。

> **记忆点**：有接口 JDK，无接口 CGLIB；Boot 2 起统一 CGLIB；final 类不行。

#### 追问：同一个类里 A 方法调用 B 方法，B 上的 @Transactional / @Cacheable 会生效吗？

不会。因为 this.b() 是目标对象内部调用，不经过代理，AOP 拦截不到。解决：① 把 B 抽到另一个 Bean 里调用；② 注入自身代理（@Lazy 或 AopContext.currentProxy()，需开 exposeProxy=true）；③ 用 TransactionTemplate 显式编程式事务。这就是「AOP 只对代理入口生效」的经典坑。

### Q034 ★★★ 高 Spring 事务的传播行为有哪几种？

七种，最常用三个：REQUIRED（默认，有事务就加入，没有就新建）、REQUIRES_NEW（总是新建，挂起外部事务）、NESTED（嵌套，用 savepoint，外部回滚会连带回滚）。

| 传播行为 | 有外层事务时 | 无外层事务时 | 典型场景 |
| --- | --- | --- | --- |
| REQUIRED（默认） | 加入 | 新建 | 绝大多数业务 |
| REQUIRES_NEW | 挂起外层，新建独立事务 | 新建 | 记录日志、发通知，不受主流程回滚影响 |
| NESTED | 建 savepoint 子事务 | 新建 | 部分失败可单独回滚 |
| SUPPORTS | 加入 | 不用事务 | 查询 |
| NOT_SUPPORTED | 挂起外层 | 不用事务 | 必须非事务的操作 |
| MANDATORY | 加入 | 抛异常 | 强制要求在事务中 |
| NEVER | 抛异常 | 不用事务 | 禁止在事务中 |

- REQUIRES_NEW 的关键：内层事务提交后，外层回滚不会回滚内层（这就是「记日志不受主流程影响」的实现方式），但要注意连接会占两个，嵌套太深容易耗尽连接池。
- NESTED 依赖数据库的 savepoint 支持（MySQL InnoDB 支持），外层回滚会连带内层。

> **记忆点**：REQUIRED 加入，REQUIRES_NEW 独立，NESTED 存盘回滚分段。

#### 追问：REQUIRES_NEW 和 NESTED 的本质区别？

REQUIRES_NEW 是两个独立事务（两个连接），外层回滚不影响内层，内层回滚也不影响外层；NESTED 是同一个事务内的 savepoint（同一个连接），内层回滚只回滚到 savepoint，但外层一旦回滚，内层的已提交部分也会丢。所以「必须留痕」用 REQUIRES_NEW，「部分失败只回滚一段」用 NESTED。

### Q035 ★★★ 极高 @Transactional 什么情况下会失效？

六种高频失效：① 同类内部方法直接调用（不走代理）；② 方法不是 public（CGLIB 下 private/final 无法代理）；③ 异常被自己 catch 了没抛出；④ 抛的是受检异常（默认只回滚 RuntimeException 和 Error）；⑤ 类没被 Spring 管理（自己 new 的）；⑥ 数据库引擎不支持事务（MyISAM）。

- 显式指定回滚异常：@Transactional(rollbackFor = Exception.class)，这是写业务代码的标配。
- @Transactional 加在接口上时，CGLIB 代理可能不生效（Boot 2 起统一 CGLIB，加在实现类的方法上更稳）。
- 多数据源时事务管理器要指定 transactionManager，否则可能用错。
- @Transactional 遇到 try-catch：要么重新抛出，要么手动 TransactionAspectSupport.currentTransactionStatus().setRollbackOnly()。

> **记忆点**：自调用、非 public、被 catch、受检异常、非 Bean、引擎不支持——六个失效点。

#### 追问：为什么默认只对 RuntimeException 回滚？怎么改？

这是 Spring 的约定：受检异常通常表示「可预期的业务分支」（如余额不足），调用方可能想继续处理；非受检异常表示程序错误，应当整体回滚。改法：@Transactional(rollbackFor = Exception.class)，或在 XML/配置里改 rollbackOn。

### Q036 ★★★ 极高 Spring Boot 自动装配的原理？

靠 @SpringBootApplication 里的 @EnableAutoConfiguration → @Import(AutoConfigurationImportSelector.class)，它在启动时读取所有 jar 包 META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports（Boot 2.7 之前是 spring.factories）里声明的自动配置类，再按 @Conditional 系列注解做条件筛选，满足条件的才注册 Bean。

- 三大条件注解：@ConditionalOnClass（类路径有某个类才生效）、@ConditionalOnMissingBean（用户没自己定义才生效，这是「约定优于配置 + 可覆盖」的关键）、@ConditionalOnProperty（配置开关）。
- 自动配置类本身用 @AutoConfiguration + @EnableConfigurationProperties，把 application.yml 的配置绑定到 @ConfigurationProperties 类。
- 加载顺序：@AutoConfiguration 支持 before/after 排序，用户自定义 Bean 优先于自动配置。
- 自定义 starter：写配置类 + AutoConfiguration.imports 文件 + 自动配置属性类，打成 jar 即可。
- 调试：--debug 启动会打印 CONDITIONS EVALUATION REPORT，能看到哪些自动配置生效、为什么没生效。

> **记忆点**：@EnableAutoConfiguration → 读 imports 文件 → 条件注解筛选 → 注册 Bean。

#### 追问：Spring Boot 2.7 / 3.0 在自动装配上有什么变化？

2.7 引入 AutoConfiguration.imports 文件替代 spring.factories（后者在 3.0 被移除），目的是把「自动配置」和「其他扩展点（如 EnvironmentPostProcessor、Listener）」解耦，启动更快、更清晰。3.0 还把 javax.\* 迁移到 jakarta.\*，并要求 JDK 17+。

### Q037 ★★★ 极高 过滤器、拦截器、AOP 的区别？

三者处于请求处理链的不同层次：Filter 属于 Servlet 容器，拦截所有请求（包括静态资源），最早执行；Interceptor 属于 Spring MVC，在 DispatcherServlet 内、Handler 前后执行，能拿到 HandlerMethod；AOP 属于方法级，能拦截任意 Bean 方法，不限于 Web 请求。

| 维度 | Filter | Interceptor | AOP |
| --- | --- | --- | --- |
| 所属 | Servlet 规范 | Spring MVC | Spring AOP |
| 作用范围 | 所有请求 | Controller 请求 | 任意 Bean 方法 |
| 能否拿到方法信息 | 否 | 能（HandlerMethod） | 能（Method + 参数） |
| 典型用途 | 编码、跨域、XSS 过滤、请求日志 | 登录校验、权限、日志 | 事务、缓存、幂等、限流 |

- 执行顺序：Filter → Interceptor.preHandle → AOP → Controller → AOP → Interceptor.postHandle/afterCompletion → Filter。
- 你简历里「自定义注解 + AOP 做角色鉴权」属于 AOP 层，能拿到方法上的注解参数；如果只是拦 URL 用拦截器更轻。
- 拦截器里抛异常不会回滚事务（事务在 Service 层），这也是鉴权通常前置到拦截器/AOP 的原因。

> **记忆点**：Filter 在外层管请求，Interceptor 在 MVC 层管 Handler，AOP 在方法层管 Bean。

#### 追问：为什么鉴权通常放在拦截器或 AOP，而不是 Filter？

Filter 只能拿到 HttpServletRequest，拿不到「要执行哪个 Controller 方法、方法上有什么注解」，无法做细粒度的注解式权限（@RequireRole("ADMIN")）。拦截器能拿到 HandlerMethod，AOP 能拿到方法参数，所以「注解 + 鉴权」需要它们。但如果是「统一登录态校验」，Filter 也完全够用，且能覆盖非 MVC 的请求。

## 六、MyBatis

### Q038 ★★★ 极高 #{} 和 ${} 的区别？

\#{} 是预编译占位符，最终变成 ?，用 PreparedStatement 设置参数，能防 SQL 注入；${} 是字符串直接拼接，原样拼进 SQL，有注入风险。能用 #{} 就一定用 #{}。

- #{} 会按参数类型做 JDBC 类型推断，字符串自动加引号；${} 不加引号，所以字符串要自己写 '${xxx}'。
- #{} 可以指定 javaType、jdbcType、typeHandler；${} 不行。
- ${} 的合法场景：动态表名、动态列名、ORDER BY 字段、LIMIT 偏移 —— 这些是 SQL 结构的一部分，无法用 ? 占位。
- 用 ${} 时必须在 Java 层做白名单校验（表名/字段名枚举），绝不能直接透传前端参数。
- 面试延伸：ORDER BY ${sortField} 是最常见的注入点，正确做法是枚举校验后用 #{} 已不可行，所以要白名单。

> **记忆点**：#{} 预编译防注入，${} 直接拼；${} 只用于表名列名排序，必须白名单。

#### 追问：为什么 ORDER BY 不能用 #{}？

因为 #{} 会被替换成 ?，而 JDBC 的预编译参数只能绑定值，不能绑定 SQL 的语法结构（标识符、关键字）。ORDER BY ? 会被数据库当成「按常量排序」，语法上也非法。所以只能拼字符串，但必须做白名单校验。

### Q039 ★★★ 高 MyBatis 的一级缓存和二级缓存？

一级缓存是 SqlSession 级别的，默认开启，用 PerpetualCache + HashMap 存，同一 SqlSession 内相同 SQL 与参数会命中；二级缓存是 Mapper（namespace）级别的，默认关闭，需要 cacheEnabled=true + Mapper 里加 \<cache/\> 才生效，跨 SqlSession 共享。

- 一级缓存失效场景：SqlSession 关闭、执行了 insert/update/delete（任意写操作会清空整个一级缓存）、手动 clearCache()、事务提交/回滚（Spring 下每个事务一个 SqlSession）。
- 二级缓存问题：跨 namespace 的写不会清空别的 namespace 的缓存，多表关联时容易读到脏数据；所以生产环境基本不开二级缓存，改用 Redis 自己控制。
- 二级缓存需要实体实现 Serializable（可配置为内存引用，但默认可能序列化）。
- Spring 集成下，没有事务时每次查询都是新 SqlSession，一级缓存直接失效——这是「明明同一个方法为什么没命中缓存」的常见原因。

> **记忆点**：一级 SqlSession 默认开，写就清空；二级 namespace 默认关，多表会脏，生产别开。

#### 追问：一级缓存和 Spring 事务有什么关系？

Spring 用 SqlSessionTemplate 管理 SqlSession，在一个事务内复用同一个 SqlSession，所以一级缓存能生效；如果没有事务（autocommit），每个 Mapper 方法都会新开 SqlSession 并关闭，一级缓存相当于不存在。这也解释了「加了 @Transactional 之后某些查询行为变了」的现象。

### Q040 ★★★ 高 PageHelper 的分页原理？有什么坑？

PageHelper 是 MyBatis 插件（Interceptor），拦截 Executor.query，在执行 SQL 前拿到 Page 参数，先执行一条 SELECT COUNT(\*) 得到总数，再用数据库方言改写原 SQL 加上 LIMIT，最后把结果包装成 PageInfo。

- 原理链路：PageHelper.startPage(pageNum, pageSize) 把分页参数放进 ThreadLocal → 插件拦截到 query 时取出、清除 → 生成 count SQL 与分页 SQL。
- 关键实现类：PageInterceptor（拦截）、Page（继承 ArrayList，携带 total/pages 等）、PageInfo（封装给前端）。
- 坑 1（最经典）：startPage 必须紧跟第一条查询语句，中间不能插入其他查询，否则分页会作用到错误的那条 SQL 上（因为参数在 ThreadLocal 里，谁先执行谁消费）。
- 坑 2：count 查询在复杂 SQL（多表 join、group by）下可能很慢或结果不准，可关掉自动 count（pageHelper.count=false）自己写 count。
- 坑 3：ThreadLocal 没清理会污染后续请求（PageHelper 在 finally 里 clear，但如果查询抛异常前未消费，可能残留）。
- 坑 4：和 foreach/复杂子查询混用偶发改写错误，需要看日志确认最终 SQL。

> **记忆点**：插件拦 Executor，先 count 再 LIMIT，参数走 ThreadLocal，startPage 必须紧跟查询。

#### 追问：为什么用 PageHelper 而不是直接写 LIMIT？

PageHelper 的优势是「业务代码不感知分页」，自动算 total 并适配不同数据库方言；缺点是隐式行为（ThreadLocal）容易踩坑，且 count SQL 未必最优。数据量大、SQL 复杂的场景（如报表）我更倾向手写 count + limit，可控性更好。

## 七、MySQL

### Q041 ★★★ 极高 为什么 MySQL 索引用 B+ 树而不是 B 树、红黑树、哈希？

因为 B+ 树非叶子节点只存键不存数据，单页能放更多索引项，树更矮（3 层可支撑约 2000 万行），磁盘 IO 更少；且叶子节点用双向链表相连，范围查询和排序只需顺序扫描，不像 B 树要中序遍历回溯。

- 对比哈希索引：等值查询 O(1) 很快，但不支持范围查询、排序、最左前缀，还会因冲突退化。
- 对比红黑树/二叉搜索树：每个节点只存一个键，树高 log₂n，1000 万行要 20 多层，每层一次磁盘 IO，不可接受。
- 对比 B 树：B 树的非叶子节点也存数据，单页能放的键更少，树更高；且范围查询需要在树中反复上下移动。
- B+ 树叶子节点存的是完整行数据（聚簇索引）或主键值（二级索引），非叶子只存「索引列 + 子页指针」。
- 为什么是 3 层 ≈ 2000 万：InnoDB 页 16KB，非叶子节点一条索引项约 13 字节（bigint 8 + 指针 6，取整），一页可放约 1170 个；叶子页一行按 1KB 算可放 16 行。3 层 = 1170 × 1170 × 16 ≈ 2190 万行。

> **记忆点**：B+ 树矮胖 + 叶子有链表；3 层 = 1170×1170×16 ≈ 2000 万，3 次 IO 能查到。

#### 追问：为什么非叶子节点不存数据就能存更多？具体算一下。

InnoDB 一页 16KB。若存整行（假设 1KB），一页只能放 16 条，扇出只有 16；若只存「主键 + 6 字节页指针」，一页能放 16KB / 14B ≈ 1170 个键。扇出从 16 提到 1170，树高就从 6 层降到 3 层，IO 次数直接减半以上。

### Q042 ★★★ 极高 聚簇索引和二级索引有什么区别？什么是回表？

聚簇索引（主键索引）的叶子节点存整行数据，一张表只有一个；二级索引（普通索引）的叶子节点存的是索引列 + 主键值，查到主键后还要再回聚簇索引查整行，这一步叫回表。

- InnoDB 必须有聚簇索引：有主键用主键；没主键找第一个非空唯一索引；都没有则隐式生成 6 字节 row_id。
- 回表代价：一次二级索引查询 + N 次聚簇索引查询（N = 命中行数），是随机 IO。
- 避免回表：用覆盖索引（查询的列全在索引里），或用主键查询。
- 为什么二级索引不直接存行数据：太占空间、维护成本高（每次更新都要改所有索引的行数据副本）。
- MyISAM 是非聚簇索引，索引和数据分离，叶子存的是行地址。

> **记忆点**：聚簇索引叶子存整行，二级索引叶子存主键；拿主键再查一次就是回表。

#### 追问：为什么推荐用自增主键而不是 UUID？

① 自增主键是顺序写入，B+ 树只在右侧追加，页分裂少；UUID 随机写入会频繁触发页分裂与页合并，插入性能差、碎片多。② 自增主键 8 字节，UUID（字符串 36 字节）更长，二级索引里每个叶子都要存主键，索引体积膨胀更明显。若必须用无序 ID，用雪花算法（有序 bigint）折中。

### Q043 ★★★ 高 什么是覆盖索引？怎么判断用上了？

一条查询需要的数据全部能从索引里拿到，不需要回表，就叫覆盖索引。EXPLAIN 的 Extra 出现 Using index 就表示命中了覆盖索引。

- 例子：idx_name_age(name, age)，查 SELECT name, age FROM t WHERE name = 'x' 就是覆盖索引。
- 价值：省掉回表，减少随机 IO 与锁竞争，是最高性价比的优化手段之一。
- 坑：SELECT \* 几乎不可能覆盖索引；把常用查询列加进联合索引可以做「索引覆盖优化」。
- 区分：Using index 是覆盖索引；Using index condition 是索引下推（ICP），仍可能回表，两者不同。

> **记忆点**：要的列全在索引里 = 覆盖索引 = Using index；SELECT \* 永远不是。

#### 追问：Using index 和 Using index condition 有什么区别？

Using index 表示「不回表，索引里就有全部数据」（覆盖索引）。Using index condition 表示用到了索引下推：在存储引擎层就用索引列做条件过滤，减少回表的行数，但最终仍需要回表取其他列。ICP 是 MySQL 5.6 引入的优化。

### Q044 ★★★ 极高 什么是最左前缀原则？哪些情况索引会失效？

联合索引 (a, b, c) 的排序是先按 a、再按 b、再按 c，所以查询条件必须从最左列开始且不跳过中间列才能用上索引。索引失效的典型情况：函数/运算包住索引列、隐式类型转换、LIKE '%x' 前导模糊、OR 连接非索引列、!=/NOT IN 有时失效、范围查询之后的列失效。

- 能用：a、a,b、a,b,c、a + c（c 用不上索引但 a 能用，ICP 可能帮上忙）。
- 不能用：b、c、b,c（跳过最左列）。
- 失效 1：WHERE DATE(create_time) = '2024-01-01' → 改成范围：create_time \>= '2024-01-01' AND \< '2024-01-02'。
- 失效 2：WHERE phone = 13800000000（phone 是 varchar，传数字）→ 隐式类型转换，索引失效并可能扫描全表。
- 失效 3：WHERE name LIKE '%张%' → 无法用索引，只能改为前缀 '张%' 或走全文/ES。
- 失效 4：WHERE a = 1 OR b = 2 且 b 无索引 → 全表扫描。
- 失效 5：范围查询后的列失效——WHERE a \> 1 AND b = 2，(a,b) 索引中 b 用不上（5.6+ 可用 ICP 过滤，但仍不回表优化）。
- 不失效的例外：!=、NOT IN 是否失效取决于优化器对回表率与全表扫描成本的估算，不能一概而论。

> **记忆点**：最左不跳列；函数、类型转换、前导 %、OR、范围后续列——五个失效点。

#### 追问：为什么隐式类型转换会让索引失效？

索引是按字符串的排序规则（collation）建的。当 varchar 列与数字比较时，MySQL 要把索引列转成数字再比较，等于对索引列加了函数 CAST(col AS SIGNED)，索引的有序性被破坏，只能全表扫描。反过来，int 列与字符串比较时是把常量转成数字，索引仍可用（这也是「列类型 vs 常量类型，谁被转换」的细节）。

### Q045 ★★★ 高 EXPLAIN 关键字段怎么看？

重点看五个字段：type（访问类型，衡量好坏）、key（实际用的索引）、rows（预估扫描行数）、Extra（是否回表/排序/临时表）、key_len（联合索引用到了几列）。

- type 好坏排序：system \> const \> eq_ref \> ref \> range \> index \> ALL。出现 index（全索引扫描）和 ALL（全表扫描）就要优化。
- key 为 NULL 说明没走索引；possible_keys 有但 key 为 NULL 说明优化器放弃了它（常因回表率太高）。
- Extra 常见值：Using index（覆盖索引，好）、Using where（服务层过滤）、Using temporary（用了临时表，常见于 GROUP BY，需优化）、Using filesort（额外排序，可能需加索引）、Using index condition（ICP）。
- rows 是估算值不是精确值，结合 filtered 列可估算实际返回行数。
- 进阶：EXPLAIN ANALYZE（8.0.18+）会真实执行并给出实际耗时与行数，EXPLAIN FORMAT=JSON 能看到成本模型细节。

> **记忆点**：type 看访问方式，key 看有没有用索引，rows 看扫多少，Extra 看回表排序临时表。

#### 追问：type = index 和 ALL 有什么区别？哪个更好？

ALL 是全表扫描，要读聚簇索引的所有叶子页（整行数据）；index 是全索引扫描，只读某个二级索引的所有叶子（数据量小得多），但仍是全量扫描、无法用于快速定位。两者都属于「需要优化」的级别，但 index 通常比 ALL 便宜，尤其当索引是覆盖索引时。

### Q046 ★★★ 极高 事务的 ACID 是怎么实现的？

A（原子性）靠 undo log（回滚日志，记录反向操作）；C（一致性）是目标，由 A、I、D 共同保证；I（隔离性）靠锁 + MVCC；D（持久性）靠 redo log（WAL，先写日志再写数据页）。

- undo log：记录数据的旧版本，既用于回滚（原子性），也用于 MVCC 的版本链读取。
- redo log：物理日志，记录「某页某偏移改成了什么」，顺序写，保证崩溃后能重放恢复（持久性）。
- 锁：行锁/间隙锁保证并发写不互相污染；MVCC 让读不加锁也能读一致性快照。
- 一致性是「结果」，不是某个机制：转账前后总额不变，需要应用层 + 数据库共同保证（如约束、事务）。
- 面试加分点：先写 redo log 再刷脏页（WAL）是因为 redo 是顺序写、成本低，而数据页是随机写；崩溃时用 redo 重放未刷盘的事务。

> **记忆点**：A 靠 undo，D 靠 redo，I 靠锁 + MVCC，C 是目的。

#### 追问：为什么需要 redo log，直接写数据页不行吗？

InnoDB 以页（16KB）为单位读写，一个事务可能只改几行，但直接写数据页会变成随机写 + 可能写半页。redo log 是顺序追加的小记录，成本低得多，事务提交只需保证 redo 落盘（innodb_flush_log_at_trx_commit=1），数据页可以异步刷。崩溃后用 redo 重放即可恢复，这就是 WAL（Write-Ahead Logging）。

### Q047 ★★★ 极高 四种隔离级别分别解决什么问题？MySQL 默认是哪个？

读未提交（脏读）→ 读已提交（解决脏读）→ 可重复读（解决不可重复读，MySQL 默认） → 串行化（解决幻读）。MySQL InnoDB 默认 RR（可重复读），并且通过 MVCC + 间隙锁 在 RR 下也基本解决了幻读。

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
| --- | --- | --- | --- |
| 读未提交 RU | 可能 | 可能 | 可能 |
| 读已提交 RC | 不可能 | 可能 | 可能 |
| 可重复读 RR（默认） | 不可能 | 不可能 | InnoDB 下基本不可能 |
| 串行化 | 不可能 | 不可能 | 不可能 |

- 脏读：读到了别的事务未提交的数据。
- 不可重复读：同一事务内两次读同一行，结果不同（别人改了并提交）。
- 幻读：同一事务内两次范围查询，行数不同（别人插入并提交）。
- 串行化：读加共享锁、写加排他锁，等于串行执行，性能最差。
- 为什么 MySQL 默认 RR 而 Oracle 默认 RC：历史与主从复制（statement 格式下 RR 更安全），RR 配合 MVCC 性能也不错。

> **记忆点**：RU 脏、RC 不重复、RR 不幻、串行全解决；MySQL 默认 RR。

#### 追问：RR 和 RC 在加锁上有什么不同？

RC 下每条 SQL 执行完就释放不符合条件的行锁（没有间隙锁），所以并发度高但可能出现幻读；RR 下行锁持有到事务结束，并且会有间隙锁/临键锁来防止幻读，并发度较低，死锁概率也更高。所以很多互联网公司会把隔离级别调成 RC 来降低锁冲突（阿里部分团队就这么做）。

### Q048 ★★★ 极高 MVCC 的原理是什么？ReadView 里有什么？

MVCC 让「读」不加锁也能读到一致性快照：每行有隐藏的 DB_TRX_ID（最后修改它的事务 id）和 DB_ROLL_PTR（指向 undo log 的版本链），读时根据 ReadView 判断哪个版本对本事务可见，从版本链里挑出可见的最新版本。

- 版本链：undo log 把每次修改的旧值串成链表，DB_ROLL_PTR 就是链指针。
- ReadView 四个核心字段：m_ids（活跃事务 id 集合）、min_trx_id（最小活跃事务 id）、max_trx_id（下一个将分配的事务 id）、creator_trx_id（当前事务 id）。
- 可见性判断：行的 trx_id \< min_trx_id → 可见（已提交）；\>= max_trx_id → 不可见（ReadView 之后才开的事务）；落在中间则看是否在 m_ids 里，在里面说明还活跃 → 不可见，不在 → 可见。
- RC 与 RR 的唯一区别：RC 每次 SELECT 都新建 ReadView（所以能看到别人新提交的数据）；RR 只在第一次 SELECT 时建一次 ReadView，之后复用（所以可重复读）。
- 快照读（普通 SELECT）走 MVCC；当前读（SELECT ... FOR UPDATE、UPDATE、DELETE）走锁 + 读最新版本。

> **记忆点**：版本链 + ReadView；RC 每次建、RR 建一次；四个字段记 m_ids/min/max/creator。

#### 追问：MVCC 能解决幻读吗？

不能完全解决。MVCC 只对快照读有效（读的是历史快照，看不到新插入的行）；如果是当前读（SELECT ... FOR UPDATE、UPDATE），需要靠间隙锁（Gap Lock） 阻止其他事务在区间内插入。所以 InnoDB 的 RR 是「快照读靠 MVCC + 当前读靠间隙锁」两者配合才基本消除幻读。

### Q049 ★★★ 高 有哪些锁？间隙锁和临键锁是什么？

按粒度分表锁和行锁；行锁分记录锁（Record Lock，锁索引记录）、间隙锁（Gap Lock，锁索引记录之间的间隙，只存在于 RR）、临键锁（Next-Key Lock = 记录锁 + 前面的间隙锁，RR 默认加锁单位）。另外还有意向锁（IS/IX） 用于表级与行级锁的快速冲突判断。

- 记录锁：WHERE id = 1 FOR UPDATE 锁住 id=1 这条记录。
- 间隙锁：锁住 (1, 5) 这个开区间，防止别的事务插入 id=3，从而防幻读。间隙锁之间不互斥，两个事务可以同时持有同一间隙的间隙锁。
- 临键锁：左开右闭区间 (1, 5]，RR 下范围查询默认加这个。
- 意向锁：表级，IS（打算加共享行锁）、IX（打算加排他行锁），作用只是让「加表锁」时能快速判断有没有行锁，避免逐行检查。
- 加锁规则（简化版）：唯一索引等值命中 → 退化为记录锁；唯一索引等值未命中 → 间隙锁；非唯一索引/范围 → 临键锁。
- 死锁高发点：RR 下的间隙锁 + 不同加锁顺序。

> **记忆点**：记录锁锁行、间隙锁锁空、临键锁 = 记录 + 左间隙；意向锁是表级「我要加行锁」的标记。

#### 追问：为什么 RR 下「唯一索引等值查询命中」只加记录锁而不加间隙锁？

因为唯一索引等值查询最多命中一行，不存在「范围内多出其他行」的可能，不需要间隙锁就能防幻读。这是 InnoDB 的优化：能不加间隙锁就不加，以降低锁冲突。而范围查询或非唯一索引无法保证唯一性，就必须加临键锁。

### Q050 ★★★ 高 redo log、undo log、binlog 有什么区别？为什么要两阶段提交？

三者归属不同：redo log 是 InnoDB 引擎层的物理日志（崩溃恢复，循环写、固定大小）；undo log 是 InnoDB 的逻辑日志（回滚 + MVCC 版本链）；binlog 是 MySQL Server 层的逻辑日志（记录所有变更语句，用于主从复制与数据恢复，追加写）。两阶段提交是为了保证 redo log 与 binlog 的一致性。

| 日志 | 层级 | 内容 | 写入方式 | 作用 |
| --- | --- | --- | --- | --- |
| redo log | InnoDB 引擎 | 物理页修改 | 循环写，固定大小 | 崩溃恢复（持久性） |
| undo log | InnoDB 引擎 | 反向逻辑操作 | 追加 | 回滚 + MVCC |
| binlog | Server 层 | 逻辑 SQL / 行变更 | 追加，可归档 | 主从复制、备份恢复 |

- 两阶段提交流程：① 写 redo log 并标记 prepare；② 写 binlog；③ 写 redo log 标记 commit。
- 崩溃恢复判断：redo 是 prepare 且 binlog 完整 → 提交；redo 是 prepare 但 binlog 不完整 → 回滚。
- 为什么需要：如果先写 redo 后写 binlog 且中间崩溃，主库已提交但 binlog 没有，从库就会丢数据，主从不一致。
- binlog 格式：STATEMENT（记 SQL，可能不一致）、ROW（记行变更，推荐）、MIXED。
- 组提交（group commit）：多个事务的 binlog 一起 fsync，提升吞吐。

> **记忆点**：redo 管崩溃恢复（物理），undo 管回滚与 MVCC（逻辑），binlog 管复制与备份（Server 层）；两阶段提交保两者一致。

#### 追问：innodb_flush_log_at_trx_commit 和 sync_binlog 怎么配？

innodb_flush_log_at_trx_commit=1 表示每次事务提交都把 redo 刷盘（最安全，性能最低）；sync_binlog=1 表示每次提交都把 binlog 刷盘。两者都设 1 就是「双 1 配置」，金融级场景必须这么配，性能会低一些。要求高性能且可容忍极少丢数据时分别设 2 / 100 折中，但绝不建议设为 0。

### Q051 ★★★ 极高 慢 SQL 怎么优化？给出完整套路。

五步：① 定位（慢查询日志 / performance_schema / APM）；② EXPLAIN 看执行计划，找到 type=ALL、key=NULL、rows 过大、Using filesort/Using temporary 的点；③ 优化索引（加/改联合索引、覆盖索引、消除索引失效）；④ 优化 SQL（避免 SELECT \*、深分页改游标、大事务拆分、IN 改 join）；⑤ 仍不行就改架构（缓存、读写分离、分库分表、异步化）。

- 慢查询日志：slow_query_log=ON，long_query_time=1，用 mysqldumpslow 或 pt-query-digest 聚合分析。
- 加索引优先级：WHERE / JOIN / ORDER BY / GROUP BY 涉及的列，按区分度高的在前。
- 排序优化：ORDER BY 尽量走索引顺序，避免 filesort；ORDER BY 与 WHERE 用同一个联合索引可避免排序。
- 大表 DDL：用 pt-online-schema-change 或 MySQL 8.0 的 ALGORITHM=INPLACE，避免长时间锁表。
- 打回开发的口径：单表超千万行、单 SQL 扫描行数超百万、单事务超 1 秒，都是要治理的信号。

> **记忆点**：定位 → explain → 索引 → SQL 改写 → 架构；先看 rows 和 type，再想加什么索引。

#### 追问：EXPLAIN 显示 key 有索引但查询还是很慢，可能是什么原因？

① 优化器选错了索引（统计信息过期，ANALYZE TABLE 更新，或用 FORCE INDEX 验证）；② rows 估算很小但实际回表行数巨大（没有覆盖索引，随机 IO 爆炸）；③ 索引区分度低（如性别字段），走索引不如全表扫描；④ 锁等待（innodb_lock_wait_timeout）或 Buffer Pool 太小导致磁盘读；⑤ 结果集排序/去重/临时表开销大。要用 EXPLAIN ANALYZE 或 profile 看实际耗时拆解。

### Q052 ★★★ 高 深分页为什么慢？怎么优化？

LIMIT 1000000, 10 会先扫描并丢弃前 100 万行再取 10 行，代价与偏移量成正比。优化：① 游标/延迟关联——用 WHERE id \> 上一页最大 id ORDER BY id LIMIT 10；② 子查询先取主键再关联：SELECT \* FROM t JOIN (SELECT id FROM t ORDER BY id LIMIT 1000000, 10) x USING(id)。

- 延迟关联的本质：让子查询走覆盖索引只取主键（不用回表），再用这 10 个主键回表，把 100 万次随机 IO 降为 10 次。
- 游标分页的限制：只能「上一页/下一页」，不能跳页；且排序字段必须唯一且有序。
- 业务层限制：大多数产品其实不需要跳到第 10 万页，直接限制最大页码 + 搜索结果上限，比技术优化更划算。
- 分页 count 也贵：SELECT COUNT(\*) 在无索引条件时要全表扫，可以缓存总数或用近似值。

> **记忆点**：深分页慢在「扫描丢弃」；延迟关联借覆盖索引，游标分页彻底 O(1)。

#### 追问：为什么 COUNT(\*) 比 COUNT(字段) 快？

COUNT(\*) 和 COUNT(1) 走的是最小的二级索引（或聚簇索引）统计行数，不需要判断 NULL；COUNT(字段) 要读取该字段并判断是否为 NULL（NULL 不计数），且如果字段没索引就要回表或全表读。所以 COUNT(\*) 是 MySQL 优化过的标准写法，语义也最清晰。

### Q053 ★★★ 极高 索引怎么设计？联合索引的字段顺序怎么定？

三个原则：① 区分度高的列在前（能过滤掉最多行）；② 把 WHERE 等值条件列放前面，范围/排序列放后面；③ 尽量让高频查询走覆盖索引。同时控制索引数量（写入放大、空间占用），单表 5–6 个索引为宜。

- 联合索引顺序：(a, b, c)，若查询是 a = ? AND b = ? ORDER BY c，则 a、b 等值在前、c 在最后，这样能同时用到过滤与排序。
- 区分度：COUNT(DISTINCT col) / COUNT(\*)，越接近 1 越适合做索引（如手机号、订单号）；性别这种小于 0.1 的列没必要单独建索引。
- 前缀索引：长字符串（如 URL、标题）用 INDEX(url(20))，在选择性可接受的前提下省空间。
- 最左前缀的利用：就算查询只用到 a，(a,b,c) 也能用；所以「一个联合索引顶多个单列索引」。
- 冗余索引：已有 (a,b) 就不需要 (a)；(a,b) 与 (b,a) 是不同索引，按查询模式选一个。
- 注意：UPDATE/DELETE 的 WHERE 也依赖索引，别只优化查询。

> **记忆点**：区分度高的在前，等值在前范围在后，覆盖索引优先，索引别超 5 个。

#### 追问：为什么索引不是越多越好？

① 每个索引都是一棵 B+ 树，占用磁盘与内存（Buffer Pool 里要缓存索引页）；② 每次 INSERT/UPDATE/DELETE 都要维护所有索引，写入放大；③ 优化器选择空间变大，可能选错索引；④ 频繁更新的列建索引会加剧页分裂。经验值是单表 5–6 个索引，优先用联合索引合并。

## 八、Redis

### Q054 ★★★ 极高 Redis 为什么快？为什么用单线程？

四点：纯内存操作、IO 多路复用（epoll）非阻塞、单线程避免锁竞争与上下文切换、高效的数据结构（SDS、跳表、listpack）。单线程指的是命令执行是单线程，Redis 6.0 起网络 IO 的读写已经多线程化了。

- 内存操作：数据在内存里，读写耗时是纳秒级，比磁盘快几个数量级。
- epoll：一个线程管理大量连接，事件驱动，没有「一连接一线程」的阻塞与切换开销。
- 单线程的好处：无需加锁、无并发安全问题、CPU 缓存友好、命令原子性天然保证。
- 单线程的边界：慢命令会阻塞全局（KEYS \*、FLUSHALL、大 key 的 HGETALL、DEL 大集合），所以生产要禁用/用 SCAN 替代，删除大 key 用 UNLINK。
- 6.0 的多线程：只用于 socket 读写与协议解析（io-threads），命令执行仍是单线程，因此不改变「命令原子性」的语义。

> **记忆点**：内存 + epoll + 单线程无锁 + 好数据结构；命令执行永远单线程。

#### 追问：既然单线程，Redis 怎么会成为性能瓶颈？

瓶颈通常是两类：① 网络带宽/CPU 在协议解析与序列化（所以 6.0 加了 IO 多线程）；② 慢命令阻塞（大 key、KEYS、复杂 Lua、ZRANGE 大范围）。真正的写吞吐瓶颈往往是单核 CPU 打满，此时要做集群分片而不是换多线程。

### Q055 ★★★ 极高 Redis 有哪些数据结构？底层编码是什么？

五种基础：String、Hash、List、Set、ZSet；四种扩展：Bitmap、HyperLogLog、GeoSpatial、Stream。底层编码随数据量自动切换（如 Hash 小数据用 listpack，大了转 hashtable）。

| 类型 | 底层编码 | 典型用途 |
| --- | --- | --- |
| String | int / embstr / raw（SDS） | 缓存对象、计数器、分布式锁、限流 |
| Hash | listpack → hashtable | 存对象字段（用户信息）、购物车 |
| List | listpack → quicklist | 消息队列、最新列表、栈/队列 |
| Set | intset → listpack → hashtable | 去重、共同好友（交集） |
| ZSet | listpack → skiplist + dict | 排行榜、延时队列（score 时间戳） |
| Bitmap | String 的位操作 | 签到、在线状态、布隆过滤器 |
| HyperLogLog | 概率算法 | UV 统计（误差 0.81%，12KB 固定） |
| Stream | —— | 消息队列（支持消费组、ACK） |

- SDS（简单动态字符串）：记录 len 和 free，O(1) 取长度、二进制安全、预分配减少扩容。
- ZSet 用跳表 + 字典：字典保证 O(1) 按成员查分数，跳表保证 O(log n) 按分数范围查与排序。
- 为什么用跳表不用红黑树：跳表实现简单、范围查询天然有序链表、并发场景更好改（Redis 单线程其实无所谓，但代码更简洁）。
- 版本注意：Redis 7.0 起 Hash/List/ZSet 的小对象编码统一为 listpack（替代 ziplist）。

> **记忆点**：五基础 + 四扩展；ZSet = 跳表 + 字典；Bitmap 省空间，HLL 算 UV。

#### 追问：跳表和红黑树都能做有序结构，为什么 ZSet 选跳表？

① 范围查询更简单：跳表底层是有序链表，ZRANGE 只需定位后顺链走；红黑树要做中序遍历。② 实现与维护简单，插入删除只改局部指针，不用旋转。③ 内存与性能可通过 p（层数概率）调节，实现灵活。④ Redis 单线程，不需要考虑并发安全，跳表的并发优势虽用不上，但简洁性依然占优。

### Q056 ★★★ 高 Redis 的持久化机制？RDB 和 AOF 怎么选？

RDB 是快照（二进制、体积小、恢复快、但会丢最后一段数据）；AOF 是命令追加日志（可配置 appendfsync 策略、数据更安全、但文件大、恢复慢）。生产推荐 混合持久化（RDB + AOF）：AOF 重写时以 RDB 格式写基础快照，后面追加增量命令。

- RDB 触发：SAVE（阻塞主线程，禁用）、BGSAVE（fork 子进程）、配置 save 900 1 等。
- fork 的代价：fork 本身会短暂阻塞，且写时复制（COW） 在大量写入时会翻倍占用内存，所以单机内存不要超过物理内存的一半。
- AOF 三种 fsync：always（每条命令都刷盘，最安全最慢）、everysec（每秒刷，默认，最多丢 1 秒）、no（交给 OS，最快但可能丢很多）。
- AOF 重写：BGREWRITEAOF 用最小命令集重写，解决 AOF 膨胀；auto-aof-rewrite-percentage 控制触发。
- 4.0+ 混合持久化：aof-use-rdb-preamble yes，重启时先加载 RDB 部分再重放 AOF 增量，兼顾速度与安全。
- 选择口径：纯缓存可以只开 RDB 甚至不持久化（从库重建）；有业务数据必须开 AOF everysec + RDB 备份。

> **记忆点**：RDB 快照快恢复但会丢，AOF 日志安全但慢；生产用混合持久化。

#### 追问：BGSAVE 时主线程还能处理请求吗？为什么？

能。BGSAVE 用 fork() 创建子进程，子进程持有 fork 时刻的内存快照，子进程负责把数据写盘，主线程继续处理请求。但 fork 本身会阻塞主线程（拷贝页表，内存越大越久），而且父进程写数据时触发写时复制，会额外申请内存页，内存压力大的实例要注意。

### Q057 ★★★ 极高 Redis 的过期删除策略和内存淘汰策略？

过期删除用惰性删除 + 定期删除组合（不保证立即删除）；内存满时按 maxmemory-policy 淘汰，共 8 种：noeviction、allkeys-lru、allkeys-lfu、allkeys-random、volatile-lru、volatile-lfu、volatile-random、volatile-ttl。

- 惰性删除：访问 key 时检查是否过期，过期就删。缺点：不访问的 key 永远占内存。
- 定期删除：每 100ms 随机抽查一部分设置了过期时间的 key，删掉过期的，限制耗时不超过 25%。
- LRU（最近最少使用）：Redis 用近似 LRU（采样 maxmemory-samples 个 key，淘汰最久未使用的），不维护完整链表以省内存。
- LFU（最不经常使用）：按访问频次淘汰，4.0 引入，适合「偶发批量扫描会冲掉热点」的场景。
- volatile-\* 只淘汰设置了过期时间的 key；allkeys-\* 淘汰所有 key。
- 生产建议：纯缓存用 allkeys-lru 或 allkeys-lfu；有重要数据用 volatile-lru 并配合持久化。

> **记忆点**：过期 = 惰性 + 定期；淘汰 8 种 = 4 策略 ×（allkeys/volatile）+ noeviction。

#### 追问：为什么 Redis 的 LRU 是「近似」的？有什么影响？

维护一个完整的双向链表需要在每次访问时移动节点、加锁（多线程下），内存和 CPU 开销都大。Redis 采用采样法：随机取 N 个 key，从中挑空闲时间最长的淘汰。缺点是可能淘汰掉实际还热但没被采到的 key；官方测试表明 maxmemory-samples=5 就接近真实 LRU，=10 时误差很小。

### Q058 ★★★ 极高 缓存穿透、缓存击穿、缓存雪崩分别是什么？怎么解决？

穿透=查不存在的数据，缓存和 DB 都没有，请求全打 DB；击穿=某个热点 key 过期瞬间，大量请求打 DB；雪崩=大批 key 同时过期或 Redis 宕机，DB 被打挂。

| 问题 | 本质 | 解决方案 |
| --- | --- | --- |
| 穿透 | 数据不存在，缓存永远不命中 | ① 缓存空值（短 TTL）；② 布隆过滤器提前拦截；③ 接口参数校验、限流 |
| 击穿 | 单个热点 key 失效瞬间 | ① 互斥锁/分布式锁重建缓存；② 逻辑过期（不设 TTL，异步刷新）；③ 热点永不过期 |
| 雪崩 | 大量 key 同时失效 / Redis 故障 | ① TTL 加随机值打散；② 多级缓存（本地 + Redis）；③ 集群高可用（哨兵/Cluster）；④ 熔断降级、限流 |

- 布隆过滤器：用多个哈希函数映射到位数组，判断「不存在」一定准确，判断「存在」可能误判，所以适合做「白名单前置拦截」。删除困难，可用 Counting Bloom 或定时重建。
- 击穿的互斥锁写法：缓存未命中 → SETNX 抢锁 → 抢到的查 DB 并回填 → 没抢到的短暂 sleep 后重试读缓存。
- 逻辑过期：value 里存 expireTime，读到过期就打标记异步刷新，返回旧值，保证高可用但可能读到旧数据。
- 雪崩的兜底：本地缓存（Caffeine）挡住绝大部分请求，Redis 挂了也能撑一段时间。

> **记忆点**：穿透用布隆 + 空值，击穿用互斥锁 + 逻辑过期，雪崩用随机 TTL + 多级缓存。

#### 追问：为什么缓存空值要设短 TTL？能不能不设？

必须设短 TTL（如 30–60 秒），否则一旦有大量随机的不存在请求，缓存里会堆满空值，占用内存且可能长期返回错误的「不存在」（如果之后数据被创建了，用户会一直看不到）。短 TTL 是「挡住瞬时穿透」与「数据及时性」的折中。

### Q059 ★★★ 极高 缓存和数据库的一致性怎么保证？

首选 Cache Aside + 先更新数据库、再删除缓存（不是更新缓存）。这个方案在绝大多数场景够用，极端并发下的不一致窗口极小。要求强一致就用延迟双删或订阅 binlog 异步删缓存（Canal）。

- 为什么是「删」不是「更新」：更新缓存在并发下可能被旧值覆盖（两个线程的写顺序与缓存写入顺序不一致）；删除更简单，下次读自然回源。
- 为什么「先更新 DB 再删缓存」：如果先删缓存再更新 DB，中间有读请求会把旧值重新加载进缓存，导致长期脏数据；先更新 DB 则最坏情况只是短暂的旧缓存。
- 延迟双删：更新 DB 前删一次、更新后延迟（如 500ms，略大于一次读的耗时）再删一次，处理「更新期间有读请求回填旧值」的极端情况。
- binlog 方案（推荐用于重要业务）：Canal 订阅 MySQL binlog，解析出变更后删对应缓存，做到与业务代码解耦、失败可重试。
- 兜底：缓存设 TTL，即使不一致也会自动过期；对一致性要求极高的走「读写都走 DB + 本地缓存短 TTL」。

> **记忆点**：Cache Aside：先更库、再删缓存；兜底靠 TTL；强一致靠 binlog 订阅。

#### 追问：为什么不用「先删缓存，再更新数据库」？

因为这个顺序下，删完缓存到 DB 更新完成之间有一个窗口：如果此时有读请求，会读到 DB 的旧值并写回缓存，等 DB 更新完成后，缓存里就留下了旧值，且这个旧值会一直存在直到 TTL 过期，属于「长期不一致」。而「先更新 DB 再删缓存」的最坏情况只是「读到旧缓存的短暂窗口」，影响小得多。

### Q060 ★★★ 极高 Redis 分布式锁怎么实现？有哪些坑？

基础版 SET key value NX PX 30000（原子加锁 + 过期防死锁），value 存唯一标识（如 UUID），释放时用 Lua 脚本校验标识再删除（保证「判断 + 删除」原子）。生产用 Redisson：看门狗自动续期、可重入、支持公平锁与红锁。

- 为什么 value 要唯一：防止「A 的锁过期了、B 拿到了锁，A 执行完把 B 的锁删了」。所以必须 Lua 比对 value。
- 为什么必须设过期时间：防止持锁进程崩溃导致死锁。但过期时间又带来「业务没执行完锁就释放」的问题。
- 看门狗（watchdog）：Redisson 默认锁 30 秒，后台线程每 10 秒（1/3 过期时间）检查业务是否还在执行，在则续期——解决「业务超时」与「死锁」的矛盾。
- 不可重入问题：基础 SETNX 版本不可重入，同一线程再次加锁会失败；Redisson 用 Hash 结构（key → {threadId: count}）实现可重入。
- 主从架构的致命问题：主库加锁成功后还没同步到从库就宕机，从库升主后锁丢失，两个客户端同时持锁。这就是 Redlock 想解决的问题。
- 更稳妥的方案：对一致性要求极高的场景，用 ZooKeeper / etcd（基于 CP 的共识），或用数据库唯一索引兜底。

> **记忆点**：SET NX PX + 唯一 value + Lua 释放；生产上用 Redisson 看门狗。

#### 追问：Redlock 是什么？为什么有争议？

Redlock 是 Redis 作者提出的算法：向 N 个独立的 Redis 主节点（通常 5 个）依次加锁，只有在多数节点（≥ N/2+1） 加锁成功且总耗时小于锁有效期时才认为加锁成功。争议在于它依赖各节点的时钟假设（锁过期依赖本地时间推进），如果某个节点发生时钟跳跃或长时间 GC，安全性会被破坏，Martin Kleppmann 因此认为它不提供严格的安全性保证。工程上更推荐「普通主从 + 业务幂等」而不是追求 Redlock 的强一致。

### Q061 ★★★ 极高 你项目里用 Redis 做浏览量聚合，怎么保证不丢数据？

用 INCR 在 Redis 里做原子累加，定时任务（如每 30 秒）批量把增量刷进 MySQL，刷完再 DECRBY 扣除对应增量。核心是「先累加、后批量落库、落库成功再扣减」 的顺序，加上幂等与失败重试，避免重复计数或丢数。

- 为什么不在浏览器每次直接 UPDATE count = count + 1：2 万次浏览就是 2 万次行锁更新，热行锁竞争严重、redo log 暴涨。改成 Redis 聚合后 MySQL UPDATE 从 2 万次压到 1 次（这正是简历上「2 万次压成 1 次」的口径）。
- 关键实现：用 Hash 存 {projectId: delta}，定时任务 HGETALL 拿到所有增量，批量 UPDATE ... SET views = views + delta，成功后 HDEL/DECRBY 清掉对应增量。
- 防丢：刷库失败就不扣减，下一轮重试；Redis 挂了会丢最近一个周期的增量，可接受（浏览量是非核心业务）。要更稳可以加「本地内存 buffer + 定时上报」双写。
- 防重：用 HINCRBY 的返回值判断本轮增量，或用分布式锁保证同一时刻只有一个刷库任务。
- 阈值控制：如果某 key 增量超过阈值（如 1000）立即触发刷库，避免内存堆积和丢失范围过大。
- 展示时用「Redis 实时值 + MySQL 基准值」相加，保证用户看到的数是准的。

> **记忆点**：INCR 累加 → 定时批量 UPDATE → 成功后扣减；失败不扣、下轮重试。

#### 追问：如果定时任务执行期间 Redis 挂了，会怎样？

最近一个周期（最多一个刷库间隔）的增量会丢失，用户看到的浏览量会「回退」一点。解决：① 缩短刷库间隔；② 增量先写本地日志/消息队列再落库（至少一次语义 + 幂等去重）；③ 接受这个误差（浏览量本身就是近似值，产品上可容忍）。这也是我选「最终一致 + 可容忍误差」而不是强一致的原因——强一致需要每次浏览都同步写库，性能代价不可接受。

### Q062 ★★★ 极高 多级缓存怎么设计？为什么需要 Caffeine + Redis？

本地缓存（Caffeine）扛超热点、抗 Redis 网络开销，Redis 扛全量共享数据与跨实例一致性，DB 是最终数据源。读顺序：本地 → Redis → DB（回填 Redis，再回填本地）。关键是本地缓存的一致性与失效广播。

- Caffeine 用 W-TinyLFU 算法，命中率高于 LRU，支持 maximumSize、expireAfterWrite、refreshAfterWrite（异步刷新，避免击穿）。
- 本地缓存的问题：多实例之间不共享，一个实例更新了，其他实例的本地缓存还是旧的。解决：① 短 TTL（如 1–5 秒，用时间换一致性）；② 通过 Redis 发布订阅 / MQ 广播失效消息，各实例收到后失效本地 key。
- 为什么热点吞吐能提升十几倍：本地缓存是进程内内存访问（纳秒级），省掉了 Redis 的网络往返与序列化，热点 key 几乎不打 Redis。
- 数据量约束：本地缓存只能放「极热且小」的数据，内存占用要严格限制（如 maximumSize = 1000），否则会 OOM 或引发长 GC。
- 更新策略：先更 DB → 删 Redis → 广播本地失效；或用 refreshAfterWrite 做定时兜底刷新。

> **记忆点**：本地抗热点、Redis 管共享、DB 兜底；本地一致性靠短 TTL + 广播失效。

#### 追问：本地缓存会不会导致不同机器返回的数据不一致？

会。本质上本地缓存是「每实例一份副本」，无法做到强一致。工程上的处理：① 对「秒级不一致可接受」的数据（列表、配置、计数）用短 TTL；② 对「必须一致」的数据（权限、余额）不放本地缓存，或每次校验；③ 用广播失效把不一致窗口压到毫秒级。这是「性能 vs 一致性」的显式取舍，面试时要把这个 trade-off 说出来。

### Q063 ★★★ 高 大 key 和热 key 怎么发现和处理？

大 key 指 value 过大（String \> 10KB 或集合元素 \> 5000）；热 key 指单 key 的 QPS 过高（如秒杀商品）。大 key 用 redis-cli --bigkeys、MEMORY USAGE、分析 RDB 发现；热 key 用 --hotkeys（需开 LFU）、客户端统计、或在代理层（如 京东 hotkey）探测。

- 大 key 的危害：网络阻塞（一次读几百 KB）、删除阻塞（DEL 大 hash 会卡主线程，用 UNLINK 异步删）、集群倾斜（整个 key 落一个 slot）。
- 大 key 的治理：拆分成多个小 key（如 user:1:info、user:1:ext）、改用 Hash 分字段读写（HMGET）、压缩 value、把大集合拆成 list 分片。
- 热 key 的危害：单个分片 CPU 打满、集群倾斜，其他请求被拖慢。
- 热 key 的治理：① 本地缓存（最有效）；② 把热 key 复制多份（key:0、key:1…随机读）打散；③ 读写分离/多副本；④ 限流降级。
- 大 key 删除：Redis 4.0+ 用 UNLINK（后台线程释放内存），或分批 HDEL/SREM。

> **记忆点**：大 key 拆 + UNLINK 异步删；热 key 本地缓存 + 复制多份打散。

#### 追问：为什么集群模式下大 key 更危险？

Cluster 按 key 的 hash slot 分片，一个大 key 只会落在一个节点上，导致该节点内存和流量远高于其他节点，形成「数据倾斜」，扩容也无法缓解（除非改 key 设计）。所以集群对大 key 的容忍度更低，通常要求单 key \< 10KB、集合元素 \< 5000。

## 九、计算机网络与 Web

### Q064 ★★★ 极高 TCP 三次握手和四次挥手的过程？

握手三步：SYN → SYN+ACK → ACK，目的是双向确认收发能力并同步初始序列号（ISN）。挥手四次：FIN → ACK → FIN → ACK，因为 TCP 是全双工，两个方向要分别关闭。

- 握手：客户端 SYN=1, seq=x → 服务端 SYN=1, ACK=1, seq=y, ack=x+1 → 客户端 ACK=1, seq=x+1, ack=y+1。
- 挥手的中间两次不能合并：服务端收到 FIN 后先回 ACK（表示「我知道你要关了」），但自己可能还有数据要发，等发完再发自己的 FIN。
- 主动关闭方进入 TIME_WAIT，等待 2MSL 后进入 CLOSED。
- 状态流转：ESTABLISHED → FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT → CLOSED（主动方）；ESTABLISHED → CLOSE_WAIT → LAST_ACK → CLOSED（被动方）。
- 面试延伸：CLOSE_WAIT 大量堆积说明应用层没调用 close()（代码 bug），TIME_WAIT 大量堆积说明主动关闭连接太多（可用连接池、SO_REUSEADDR 缓解）。

> **记忆点**：握手 SYN / SYN+ACK / ACK；挥手 FIN / ACK / FIN / ACK；TIME_WAIT 等 2MSL。

#### 追问：为什么握手是三次而不是两次？

两次握手无法确认「客户端的接收能力」和「服务端的发送能力」：如果客户端发出的旧 SYN 在网络中滞留，延迟到达服务端，服务端会误以为客户端要建新连接并直接进入 ESTABLISHED，造成资源浪费。三次握手中客户端最后回 ACK，服务端才能确认「客户端确实收到了我的 SYN」，同时双方都确认了对方的 ISN，避免历史连接的数据污染。

### Q065 ★★★ 高 为什么挥手需要 TIME_WAIT？2MSL 是多久？

TIME_WAIT 有两个作用：① 保证最后一个 ACK 能到达对端（若 ACK 丢失，对端会重发 FIN，此时还能响应）；② 让本次连接的所有报文在网络中消散，避免影响后续复用相同四元组的新连接。2MSL 是「报文最大生存时间的两倍」，Linux 上 MSL 通常取 30 秒，所以 TIME_WAIT 约 60 秒。

- MSL（Maximum Segment Lifetime）：报文在网络中的最大存活时间，Linux 内核 TCP_TIMEWAIT_LEN 固定为 60 秒（2 × 30s）。
- 大量 TIME_WAIT 的影响：占用本地端口（约 6.4 万个），高并发短连接服务端可能端口耗尽。
- 优化手段：① 用长连接/连接池（最根本）；② net.ipv4.tcp_tw_reuse=1（允许复用 TIME_WAIT 连接，仅对客户端有效）；③ 扩大端口范围 ip_local_port_range；④ 服务端作为被动关闭方可以减少主动 TIME_WAIT。
- 不要用 tcp_tw_recycle（NAT 环境下会出严重问题，Linux 4.12 起已移除）。

> **记忆点**：TIME_WAIT = 保 ACK 到 + 清残留报文；2MSL ≈ 60 秒；优化靠长连接。

#### 追问：服务端出现大量 CLOSE_WAIT 说明什么？

说明被动关闭方没有调用 close()：收到对端 FIN 后内核回了 ACK 并进入 CLOSE_WAIT，但应用层没关连接，就永远停在这个状态。这是典型的代码 bug（连接泄漏、忘了关流、异常分支没 finally），不是网络问题。排查看代码里连接是否都在 finally 中关闭。

### Q066 ★★★ 高 HTTP/1.1、HTTP/2、HTTP/3 有什么区别？

HTTP/1.1 是文本协议 + 短连接/管线化（有队头阻塞）；HTTP/2 是二进制分帧 + 多路复用 + 头部压缩（HPACK）+ 服务端推送，解决了 HTTP 层的队头阻塞；HTTP/3 基于 QUIC（UDP），解决了 TCP 层的队头阻塞，并支持 0-RTT 建连。

- HTTP/1.1 的优化手段：Connection: keep-alive 长连接、合并资源（雪碧图、打包）、域名分片（突破浏览器 6 连接限制）。
- HTTP/2 的多路复用：一个 TCP 连接上并行多个 stream，每个 stream 有 id，帧可以交错发送。
- HTTP/2 的遗留问题：TCP 层仍是单一有序流，一个包丢失会阻塞该连接上所有 stream（TCP 队头阻塞）。
- HTTP/3：QUIC 在 UDP 上实现可靠传输，天然支持多路复用且各流独立；内置 TLS 1.3，握手 1-RTT（会话恢复 0-RTT）；支持连接迁移（手机切换 WiFi/4G 不断连）。
- 注意：HTTP/2 的服务端推送（Server Push）实际已被主流浏览器废弃，因为收益不及预期。

> **记忆点**：1.1 文本 + 队头阻塞；2 二进制多路复用解决 HTTP 层；3 用 QUIC 解决 TCP 层。

#### 追问：HTTP/2 的队头阻塞和 HTTP/1.1 的有什么区别？

HTTP/1.1 的队头阻塞在应用层：前一个请求的响应没回来，后面的请求就得排队（管线化也只能串行返回）。HTTP/2 在应用层解决了（多路复用，帧可交错），但TCP 层的队头阻塞依然存在：TCP 保证字节流有序，一个 TCP 段丢失，后面所有 stream 的数据都要等重传。HTTP/3 用 QUIC 的独立流彻底解决。

### Q067 ★★★ 高 HTTPS 的握手过程？为什么能保证安全？

HTTPS = HTTP + TLS。核心是非对称加密协商出对称密钥，再用对称加密传输数据，并用证书链验证服务端身份。TLS 1.2 需要 2-RTT，TLS 1.3 优化到 1-RTT（会话恢复可 0-RTT）。

- TLS 1.2 流程：ClientHello（支持的加密套件 + 随机数）→ ServerHello（选定套件 + 随机数 + 证书）→ 客户端验证证书、用公钥加密预主密钥发送 → 双方用三个随机数算出会话密钥 → ChangeCipherSpec + Finished。
- 证书验证：浏览器用内置根 CA 公钥验签证书链，确认域名匹配、未过期、未被吊销。
- 三个随机数的作用：前两个明文随机数 + 一个用公钥加密的预主密钥，保证每次会话密钥都不同。
- 为什么用对称加密传数据：非对称加密（RSA/ECC）计算开销大，只适合协商密钥；AES 对称加密快得多，适合大数据量。
- TLS 1.3 的改进：只保留更安全的套件（废弃 RSA 密钥交换，改用 ECDHE 前向安全）、握手合并为 1-RTT、支持 0-RTT 恢复。

> **记忆点**：证书验身份，非对称换密钥，对称传数据；1.3 一次往返。

#### 追问：什么是前向安全性（Forward Secrecy）？

指服务器长期私钥泄露后，历史通信内容仍无法解密。RSA 密钥交换不具前向安全性（会话密钥由长期公钥加密，私钥泄露即可解出所有历史会话密钥）；ECDHE 临时密钥交换具备前向安全性（每次会话生成临时密钥对，用完即弃）。所以 TLS 1.3 强制使用 (EC)DHE。

### Q068 ★★★ 极高 Cookie、Session、Token、JWT 有什么区别？

Cookie 是浏览器存的键值对；Session 是服务端存的会话状态（客户端只存 sessionId）；Token 是服务端签发、客户端保存的凭证，服务端可无状态校验；JWT 是一种自包含的 Token 格式，把声明和签名都放在 token 里，服务端只需验签，不用查库。

| 方案 | 状态存哪 | 能否跨域 | 水平扩展 | 注销 |
| --- | --- | --- | --- | --- |
| Cookie | 浏览器 | 同域为主 | —— | 删 cookie |
| Session | 服务端（内存/Redis） | 需额外处理 | 需共享存储 | 删服务端状态 |
| Token/JWT | 客户端 | 天然支持 | 无状态易扩展 | 难（需黑名单） |

- JWT 结构：Header.Payload.Signature，Header 声明算法，Payload 放声明（base64 可解码，不要放敏感信息），Signature 用密钥签名防篡改。
- JWT 的缺点：无法主动失效（签发后到期前一直有效）、payload 体积大、密钥泄露风险高。解决：短有效期 + 刷新令牌 + 黑名单/版本号。
- 你简历里的「JWT 双 Token 轮换」：Access Token 短效（如 15 分钟）用于业务请求，Refresh Token 长（如 7 天）只用来换新 Access Token，且 Refresh Token 一次性使用（用完即换新的），这样即使被盗也能通过「重放检测」发现。
- 存储位置：localStorage 有 XSS 风险，HttpOnly Cookie 有 CSRF 风险，需要配合 SameSite 与 CSRF Token。

> **记忆点**：Cookie/Session 是服务端状态，Token/JWT 是客户端凭证；JWT 无状态但难注销。

#### 追问：JWT 怎么做主动注销（强制下线）？

① 黑名单：注销时把未过期的 JWT 放进 Redis（key 为 jti，TTL 设为剩余有效期），每次校验查黑名单；② 令牌版本号/白名单：用户信息里存 tokenVersion，JWT 里带上版本，改密码或强制下线时递增版本，旧 token 全部失效（需要查一次用户状态，牺牲部分无状态性）；③ 缩短 Access Token 有效期 + 依赖 Refresh Token 的可撤销性。工程上用 ② 最常见。

### Q069 ★★★ 极高 WebSocket、SSE、轮询怎么选？

轮询实现最简单但浪费请求、实时性差；SSE（Server-Sent Events） 基于 HTTP 的单向服务端推送，支持自动重连、文本协议、实现简单；WebSocket 是全双工，适合需要客户端与服务端双向实时通信的场景。

| 方案 | 方向 | 协议 | 实时性 | 复杂度 | 场景 |
| --- | --- | --- | --- | --- | --- |
| 短轮询 | 客户端拉 | HTTP | 差（取决于间隔） | 最低 | 低频状态查询 |
| 长轮询 | 客户端拉 | HTTP | 中 | 低 | 兼容性要求高的简单推送 |
| SSE | 服务端推 | HTTP/1.1 长连接 | 好 | 低 | 流式输出、进度、通知（单向） |
| WebSocket | 全双工 | 独立协议（HTTP 升级） | 最好 | 高 | 聊天、协同编辑、游戏 |

- SSE 的本质：响应头 Content-Type: text/event-stream，服务端持续写 data: xxx\n\n，浏览器 EventSource 自动解析并重连（可设 retry）。
- SSE 的限制：单向（服务端→客户端）、只支持文本（二进制要 base64）、HTTP/1.1 下有 6 连接数限制（HTTP/2 无此问题）。
- WebSocket 需要处理：握手升级（Upgrade: websocket）、心跳保活（ping/pong）、断线重连、鉴权（握手时带 token）。
- 你的项目口径：AI 流式回答用 SSE（模型输出是单向流，SSE 天然合适且能穿透大多数代理）；任务进度与通知用 WebSocket（需要握手鉴权与推送，且可能双向）。
- 选型口诀：单向流式用 SSE，双向实时用 WebSocket。

> **记忆点**：单向推 SSE（简单、自动重连），双向通信用 WebSocket，别用轮询做实时。

#### 追问：为什么大模型流式输出普遍用 SSE 而不是 WebSocket？

① 模型输出是单向流（服务端 → 客户端），SSE 的语义完全匹配，不需要双向通道；② SSE 走标准 HTTP/1.1 或 HTTP/2，能穿过大多数代理、网关、CDN，几乎不需要额外配置；③ 基于 EventSource 的自动重连和事件 id 断点续传（Last-Event-ID）天然可用；④ 实现成本比 WebSocket 低（不需要处理心跳、升级握手）。代价是只能单向、只能传文本。

### Q070 ★★★ 极高 接口幂等怎么设计？

幂等是「同一请求执行多次，结果与执行一次相同」。实现手段：唯一业务键（去重表 / 唯一索引）、幂等 Token（先取后校验）、状态机（只允许合法状态流转）、分布式锁 + 幂等表、乐观锁版本号。

- 天然幂等的操作：查询、DELETE（按 id 删）、PUT（全量覆盖）、SET 类赋值。
- 不幂等：POST 创建、UPDATE ... SET balance = balance - 100、INCR。
- 方案 1（最常用）：客户端下单前请求「获取幂等 token」，服务端存 Redis；提交时带 token，服务端用 Lua 或 SETNX 原子校验并删除，重复请求直接被拒。
- 方案 2：业务唯一键（订单号、请求 id）建唯一索引，重复插入直接失败，捕获 DuplicateKeyException 返回已有结果。
- 方案 3：状态机——订单只能「待支付 → 已支付」，重复回调发现状态已是「已支付」就直接返回成功（支付回调必须这么处理）。
- 方案 4：乐观锁 UPDATE ... SET status = 2 WHERE id = ? AND status = 1，看影响行数判断是否抢到。
- MQ 消费幂等：用消息唯一 id 做去重表，或让消费逻辑本身幂等（如「设置」而非「累加」）。

> **记忆点**：唯一键、幂等 token、状态机、乐观锁；支付回调必用状态机。

#### 追问：为什么「先查再插」不能保证幂等？

因为「查」和「插」之间有并发窗口：两个请求同时查到「不存在」，然后都插入，结果产生两条记录。必须在数据库层面靠唯一索引兜底，或用原子操作（SETNX、INSERT ... ON DUPLICATE KEY UPDATE、乐观锁 WHERE 条件），否则并发下一定失效。
