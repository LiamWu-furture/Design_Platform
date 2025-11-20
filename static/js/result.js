// 选项卡切换
function switchTab(tabName) {
    // 移除所有active类
    document.querySelectorAll('.result-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-content-item').forEach(content => {
        content.classList.remove('active');
    });
    
    // 添加active类到当前选项卡
    // 注意：这里假设调用者是 button 元素或其子元素
    const tabButton = document.querySelector(`.result-tab[onclick*="'${tabName}'"]`);
    if (tabButton) {
        tabButton.classList.add('active');
    }
    
    const tabContent = document.getElementById(tabName + '-tab');
    if (tabContent) {
        tabContent.classList.add('active');
    }
}

// 3D模型控制
let currentRotationX = -15;
let currentRotationY = 0;
let isDragging = false;
let previousMouseX = 0;
let previousMouseY = 0;

// 初始化拖动事件
document.addEventListener('DOMContentLoaded', function() {
    const scene = document.querySelector('.model-3d-scene');
    const model = document.getElementById('model3d');
    
    if (!scene || !model) return;
    
    // 鼠标事件
    scene.addEventListener('mousedown', function(e) {
        isDragging = true;
        previousMouseX = e.clientX;
        previousMouseY = e.clientY;
        scene.style.cursor = 'grabbing';
    });
    
    document.addEventListener('mousemove', function(e) {
        if (!isDragging) return;
        
        const deltaX = e.clientX - previousMouseX;
        const deltaY = e.clientY - previousMouseY;
        
        rotateWithDelta(deltaX, deltaY);
        
        previousMouseX = e.clientX;
        previousMouseY = e.clientY;
    });
    
    document.addEventListener('mouseup', function() {
        isDragging = false;
        scene.style.cursor = 'grab';
    });

    // 触摸事件 (新增)
    scene.addEventListener('touchstart', function(e) {
        if (e.touches.length === 1) {
            isDragging = true;
            previousMouseX = e.touches[0].clientX;
            previousMouseY = e.touches[0].clientY;
            e.preventDefault(); // 防止滚动页面
        }
    }, { passive: false });

    document.addEventListener('touchmove', function(e) {
        if (!isDragging || e.touches.length !== 1) return;
        
        const deltaX = e.touches[0].clientX - previousMouseX;
        const deltaY = e.touches[0].clientY - previousMouseY;
        
        rotateWithDelta(deltaX, deltaY);
        
        previousMouseX = e.touches[0].clientX;
        previousMouseY = e.touches[0].clientY;
    }, { passive: false });

    document.addEventListener('touchend', function() {
        isDragging = false;
    });

    function rotateWithDelta(deltaX, deltaY) {
        currentRotationY += deltaX * 0.5;
        currentRotationX -= deltaY * 0.5;
        
        // 限制X轴旋转角度，避免翻转过度
        currentRotationX = Math.max(-90, Math.min(90, currentRotationX));
        
        model.style.transform = `rotateX(${currentRotationX}deg) rotateY(${currentRotationY}deg)`;
    }
});

function rotateModel(direction) {
    const model = document.getElementById('model3d');
    if (!model) return;
    
    switch(direction) {
        case 'left':
            currentRotationY -= 30;
            break;
        case 'right':
            currentRotationY += 30;
            break;
        case 'up':
            currentRotationX += 15;
            currentRotationX = Math.min(90, currentRotationX);
            break;
        case 'down':
            currentRotationX -= 15;
            currentRotationX = Math.max(-90, currentRotationX);
            break;
    }
    
    model.style.transform = `rotateX(${currentRotationX}deg) rotateY(${currentRotationY}deg)`;
}

function resetModel() {
    const model = document.getElementById('model3d');
    if (!model) return;
    
    currentRotationX = -15;
    currentRotationY = 0;
    
    model.style.transform = `rotateX(${currentRotationX}deg) rotateY(${currentRotationY}deg)`;
}
