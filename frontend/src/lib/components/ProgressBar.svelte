<script lang="ts">
  export let percent: number = 0;
  $: barColor = percent >= 100 ? '#ff4d4f' : percent >= 90 ? '#ff9800' : percent >= 60 ? '#ffc107' : '#51cf66';
</script>

<div class="progress-bar-container">
  <div class="progress-bar-bg">
    <div class="progress-bar-fill" style="width: {Math.min(percent, 100)}%; background: {barColor};"></div>
  </div>
  <span class="progress-bar-label">{percent}%</span>
</div>

<style>
.progress-bar-container {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
}
.progress-bar-bg {
  flex: 1;
  height: 8px;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}
.progress-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s, background 0.3s;
}
.progress-bar-label {
  font-size: 0.85rem;
  min-width: 36px;
  text-align: right;
  color: #555;
}
</style> 