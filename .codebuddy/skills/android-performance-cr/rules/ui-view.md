# UI 渲染与流畅度（View 体系）

> §9.3 UI 渲染与流畅度 — View 体系专用规则。规则 ID 前缀 `UI-`。仅在识别到 View 体系关键字时加载。

| ID | 等级 | 检查项 | 反例 | 正例 | 判定 | 参考工具 |
|----|------|--------|------|------|------|----------|
| UI-01 | P0 | 列表必须使用 ViewHolder/等价复用 | ```kotlin
// ❌ Adapter 每项 new View
class BadAdapter : RecyclerView.Adapter<BadAdapter.VH>() {
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) =
        VH(LayoutInflater.from(parent.context).inflate(R.layout.item, parent, false))
    override fun onBindViewHolder(vh: VH, pos: Int) { /* 每次 bind new View */ }
}
``` | ```kotlin
// ✅ ViewHolder 复用
class GoodAdapter : RecyclerView.Adapter<GoodAdapter.VH>() {
    class VH(val binding: ItemBinding) : RecyclerView.ViewHolder(binding.root)
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) =
        VH(ItemBinding.inflate(LayoutInflater.from(parent.context), parent, false))
}
``` | 滑动掉帧、内存涨 | Layout Inspector |
| UI-02 | P1 | 减少布局层级与过度绘制 | ```kotlin
// ❌ 深层 LinearLayout 嵌套
<LinearLayout><LinearLayout><LinearLayout><TextView /></LinearLayout></LinearLayout></LinearLayout>
``` | ```kotlin
// ✅ ConstraintLayout 扁平化
<ConstraintLayout>
    <TextView app:layout_constraintTop_toTopOf="parent" />
</ConstraintLayout>
``` | Layout Inspector 层级 > 10 | Layout Inspector |
| UI-03 | P1 | 自定义 View onDraw 禁止分配对象 | ```kotlin
// ❌ onDraw 里 new Paint
class BadView : View {
    override fun onDraw(canvas: Canvas) {
        canvas.drawText("hello", 0f, 0f, Paint()) // 每帧 new
    }
}
``` | ```kotlin
// ✅ 成员变量复用
class GoodView : View {
    private val paint = Paint()
    override fun onDraw(canvas: Canvas) {
        canvas.drawText("hello", 0f, 0f, paint)
    }
}
``` | 滑动时 GC 频繁 | Systrace |
| UI-04 | P1 | 避免频繁 invalidate/requestLayout | ```kotlin
// ❌ 动画每帧全屏 invalidate
override fun onAnimationUpdate(animator: ValueAnimator) {
    invalidate() // 全屏重绘
}
``` | ```kotlin
// ✅ 局部刷新
override fun onAnimationUpdate(animator: ValueAnimator) {
    invalidate(animator.bounds) // 仅脏区
}
``` | Systrace 见 excessive draw | Systrace |
| UI-05 | P1 | Compose：缩小重组范围 | ```kotlin
// ❌ 大 Composable 全树重组
@Composable
fun Screen(data: Data) {
    Column {
        Header(data.title)
        Body(data.content) // Header 不需要 recompose 但也被重绘
    }
}
``` | ```kotlin
// ✅ 拆分 + @Stable
@Composable
fun Screen(data: Data) {
    Column {
        Header(title = data.title) // title 不变则不重组
        Body(content = data.content)
    }
}
``` | 重组范围过大 | Layout Inspector |
| UI-06 | P2 | 动画与硬件加速 | ```kotlin
// ❌ 软件层动画
view.setLayerType(View.LAYER_TYPE_SOFTWARE, null)
ObjectAnimator.ofFloat(view, "alpha", 1f, 0f).start()
``` | ```kotlin
// ✅ 硬件层 + clipChildren 优化
view.clipChildren = true
view.setLayerType(View.LAYER_TYPE_HARDWARE, null)
``` | GPU 过载或掉帧 | GPU 渲染分析 |
| UI-07 | P1 | Compose：remember 须带稳定 key | ```kotlin
// ❌ 无 key
@Composable
fun ItemView(item: Item) {
    val heavy = remember { computeHeavy(item) } // item 变了也不重新算
}
``` | ```kotlin
// ✅ 带 key
@Composable
fun ItemView(item: Item) {
    val heavy = remember(item.id) { computeHeavy(item) }
}
``` | 重组触发重复重计算 | Layout Inspector |
| UI-08 | P1 | RecyclerView 条目变更动画避免全量刷新 | ```kotlin
// ❌ notifyDataSetChanged 全局重绑
adapter.notifyDataSetChanged()
``` | ```kotlin
// ✅ 精确通知
adapter.notifyItemChanged(position)
adapter.notifyItemRangeInserted(start, count)
``` | 列表更新时掉帧 | Systrace |
| UI-09 | P1 | RecyclerView 大列表使用 DiffUtil 差分更新 | ```kotlin
// ❌ adapter.notifyDataSetChanged() 无动画+全局刷新
``` | ```kotlin
// ✅ ListAdapter + DiffUtil
class MyAdapter : ListAdapter<Item, VH>(ItemDiffCallback()) {
    class ItemDiffCallback : DiffUtil.ItemCallback<Item>() {
        override fun areItemsTheSame(old: Item, new: Item) = old.id == new.id
        override fun areContentsTheSame(old: Item, new: Item) = old == new
    }
}
``` | 列表更新时掉帧 | Systrace |
