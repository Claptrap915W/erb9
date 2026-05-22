// 等待页面所有HTML元素加载完成后，再执行JS功能
// 防止找不到按钮、弹窗导致报错
$(document).ready(() => {

    // ======================
    // 1. 监听：删除弹窗【即将打开】时触发
    // 作用：动态获取要删除的记录ID、删除地址，并填入弹窗
    // ======================
    $('#deleteConfirmModal').on("show.bs.modal", (e) => {
        // 获取当前点击的【删除按钮】
        const button = $(e.relatedTarget);
        
        // 从按钮的 data-id 属性中，获取要删除的咨询记录ID
        const contactId = button.data("id");
        
        // 从按钮的 data-url 属性中，获取后端删除接口地址
        const deleteUrl = button.data("url");

        // 将获取到的ID显示到弹窗提示文字中（让用户知道要删哪条）
        $("#modal-contact-id").text(contactId);
        
        // 将删除地址设置到弹窗的【确认(Yes)按钮】的href属性上
        $("#confirmDeleteBtn").attr("href", deleteUrl);
    });

    // ======================
    // 2. 监听：弹窗里的【确认删除(Yes)按钮】被点击时
    // 作用：关闭弹窗 → 延迟跳转 → 执行删除
    // ======================
    $('#confirmDeleteBtn').click((e) => {
        // 先关闭删除确认弹窗（带平滑动画）
        $("#deleteConfirmModal").modal("hide");

        // 等待300毫秒（让弹窗关闭动画完成），再跳转到删除地址
        setTimeout(() => {
            // 跳转到确认按钮上的删除链接，执行后端删除功能
            window.location.href = $("#confirmDeleteBtn").attr("href");
        }, 300);
    });

});