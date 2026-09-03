/* ============================================================
   全站交互：手机菜单 / 进场动画 / 微信复制 / 作品筛选 / 首屏视频
   ============================================================ */

// ===== 手机端菜单开关 =====
var menuToggle = document.getElementById("menuToggle");
var navLinks = document.getElementById("navLinks");
if (menuToggle && navLinks) {
  menuToggle.addEventListener("click", function () {
    navLinks.classList.toggle("open");
  });
  // 点了菜单里的链接后自动收起
  navLinks.addEventListener("click", function (e) {
    if (e.target.tagName === "A") navLinks.classList.remove("open");
  });
}

// ===== 滚动进场动画 =====
var fadeEls = document.querySelectorAll(".fade-in");
if ("IntersectionObserver" in window) {
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  fadeEls.forEach(function (el) { io.observe(el); });
} else {
  fadeEls.forEach(function (el) { el.classList.add("visible"); });
}

// 兜底：无论滚动触发是否正常，1.2 秒后全部显示，绝不让内容一直隐身
setTimeout(function () {
  fadeEls.forEach(function (el) { el.classList.add("visible"); });
}, 1200);

// ===== 微信号一键复制 =====
var copyBtn = document.getElementById("copyWechat");
if (copyBtn) {
  copyBtn.addEventListener("click", function () {
    var wechat = "X_X_0508";
    function done() {
      copyBtn.textContent = "已复制 ✓";
      setTimeout(function () { copyBtn.textContent = "复制"; }, 2000);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(wechat).then(done).catch(function () { promptCopy(); });
    } else {
      promptCopy();
    }
    // 复制失败时的兜底：弹出手动复制框
    function promptCopy() {
      window.prompt("全选复制微信号：", wechat);
      done();
    }
  });
}

// ===== 作品列表筛选 =====
var filterBar = document.getElementById("filterBar");
var workGrid = document.getElementById("workGrid");
if (filterBar && workGrid) {
  var chips = filterBar.querySelectorAll(".filter-chip");
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      chips.forEach(function (c) { c.classList.remove("active"); });
      chip.classList.add("active");
      var f = chip.getAttribute("data-filter");
      workGrid.querySelectorAll(".work-card").forEach(function (card) {
        var cat = card.getAttribute("data-cat");
        var show = (f === "all" || f === cat);
        card.style.display = show ? "" : "none";
      });
    });
  });
}

// ===== 首屏视频：视频没上传时隐藏播放器只留海报 =====
// 首屏循环播放三部王牌作品的 20 秒片段，想换顺序直接调换下面三行
var heroVideo = document.getElementById("heroVideo");
var heroStage = document.getElementById("heroStage");
var HERO_LIST = ["videos/hero-1.mp4", "videos/hero-2.mp4", "videos/hero-3.mp4"];

if (heroVideo && heroStage) {
  var heroIndex = 0;
  heroVideo.loop = HERO_LIST.length === 1;

  heroVideo.addEventListener("error", function () {
    heroVideo.style.display = "none";
    var fb = document.getElementById("heroFallback");
    if (fb) fb.hidden = false;
  });

  // 多条视频时：一条播完自动换下一条（静音循环）
  heroVideo.addEventListener("ended", function () {
    if (HERO_LIST.length < 2) return;
    heroIndex = (heroIndex + 1) % HERO_LIST.length;
    heroVideo.src = HERO_LIST[heroIndex];
    heroVideo.play().catch(function () {});
  });

  // 手机浏览器要求静音后仍需用户交互才自动播放，尽力尝试即可
  heroVideo.play().catch(function () {});
}
