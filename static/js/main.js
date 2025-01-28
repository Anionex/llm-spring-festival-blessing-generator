document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate');
    const saveImageBtn = document.getElementById('save-image');
    const recipientInput = document.getElementById('recipient');
    const requirementsInput = document.getElementById('requirements');
    const resultSection = document.querySelector('.result-section');
    const greetingText = document.getElementById('greeting-text');
    const coupletContainer = document.getElementById('couplet-container');
    const historyList = document.getElementById('history-list');
    const loading = document.getElementById('loading');

    // 移动端触摸反馈
    const addTouchFeedback = (element) => {
        element.addEventListener('touchstart', () => {
            element.style.opacity = '0.8';
        }, { passive: true });

        element.addEventListener('touchend', () => {
            element.style.opacity = '1';
        }, { passive: true });
    };

    // 为按钮添加触摸反馈
    [generateBtn, saveImageBtn].forEach(addTouchFeedback);

    // 自动调整文本框高度
    requirementsInput.addEventListener('input', () => {
        requirementsInput.style.height = 'auto';
        requirementsInput.style.height = (requirementsInput.scrollHeight) + 'px';
    });

    // 在移动端输入完成后自动隐藏键盘
    recipientInput.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') {
            recipientInput.blur();
        }
    });

    // 加载历史记录时添加动画
    async function loadHistory() {
        try {
            const response = await fetch('/api/history');
            if (!response.ok) {
                throw new Error('获取历史记录失败');
            }

            const history = await response.json();
            historyList.innerHTML = '';
            
            history.forEach((item, index) => {
                const historyItem = document.createElement('div');
                historyItem.className = 'history-item';
                historyItem.style.animation = `fadeIn 0.5s ease-out ${index * 0.1}s forwards`;
                historyItem.style.opacity = '0';
                
                historyItem.innerHTML = `
                    <p><strong>${item.recipient}</strong> - ${new Date(item.timestamp).toLocaleString()}</p>
                    <p>${item.greeting}</p>
                `;
                
                historyList.appendChild(historyItem);
            });
        } catch (error) {
            console.error('加载历史记录失败:', error);
        }
    }

    // 生成祝福
    generateBtn.addEventListener('click', async () => {
        const recipient = recipientInput.value.trim();
        const requirements = requirementsInput.value.trim();

        if (!recipient) {
            alert('请输入接收祝福的人的名字');
            recipientInput.focus();
            return;
        }

        try {
            loading.style.display = 'flex';
            // 在移动端生成时收起键盘
            if (window.innerWidth <= 768) {
                document.activeElement.blur();
            }

            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    recipient,
                    requirements
                })
            });

            if (!response.ok) {
                throw new Error('生成失败');
            }

            const data = await response.json();
            
            // 显示结果
            greetingText.textContent = data.greeting;
            coupletContainer.innerHTML = `<img src="data:image/png;base64,${data.image}" alt="春联">`;
            resultSection.style.display = 'block';
            
            // 平滑滚动到结果区域
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

            // 刷新历史记录
            loadHistory();
        } catch (error) {
            alert('生成失败: ' + error.message);
        } finally {
            loading.style.display = 'none';
        }
    });

    // 保存图片
    saveImageBtn.addEventListener('click', () => {
        const image = coupletContainer.querySelector('img');
        if (image) {
            // 检查是否为移动设备
            const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
            
            if (isMobile) {
                // 在新标签页中打开图片，用户可以长按保存
                window.open(image.src, '_blank');
            } else {
                // 桌面端使用下载方式
                const link = document.createElement('a');
                link.download = '春联.png';
                link.href = image.src;
                link.click();
            }
        }
    });

    // 初始加载历史记录
    loadHistory();

    // 处理网络状态变化
    window.addEventListener('online', () => {
        loadHistory();
    });

    // 添加页面可见性变化处理
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
            loadHistory();
        }
    });
}); 