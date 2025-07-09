<script lang="ts">
import { onMount } from 'svelte';
import { token, currentBudget } from '$lib/store';
import { getBudgets } from '$lib/apis/budgets';
import type { Budget, BudgetsGroupedResponse } from '$lib/types/budgets';
import Card from '$lib/components/Card.svelte';
import CardItem from '$lib/components/CardItem.svelte';
import FloatingButton from '$lib/components/FloatingButton.svelte';
import LoadingState from '$lib/components/LoadingState.svelte';
import EmptyState from '$lib/components/EmptyState.svelte';
import { formatCurrency, formatDate } from '$lib/utils';
import { goto } from '$app/navigation';
import IconDisplay from '$lib/components/IconDisplay.svelte';
import ProgressBar from '$lib/components/ProgressBar.svelte';
import Button from '$lib/components/Button.svelte';

export let data;
let budgetsGrouped = data.budgets ?? {};
type BudgetGroupView = { period: string; label: string; totalBudget: number; datas: Budget[] };
let budgetGroups: BudgetGroupView[] = Object.entries(budgetsGrouped).map(([period, group]) => {
  const g = group as { totalBudget: number; datas: Budget[] };
  return {
    period,
    label: getPeriodLabel(period),
    totalBudget: g.totalBudget,
    datas: g.datas
  };
});
let loading = false;
let error = '';
let activeTab: string = budgetGroups.length > 0 ? budgetGroups[0].period : '';
let activeGroup;
$: activeGroup = budgetGroups.find((g) => g.period === activeTab);

function getPeriodLabel(period: string): string {
  if (period === 'this_month') return 'This Month';
  if (period === 'this_week') return 'This Week';
  if (/\d{4}-\d{2}-\d{2}\/\d{4}-\d{2}-\d{2}/.test(period)) {
    const [start, end] = period.split('/');
    return `${formatShortDate(start)} - ${formatShortDate(end)}`;
  }
  return period;
}

function formatShortDate(dateString: string): string {
  const date = new Date(dateString);
  const day = date.getDate();
  const month = date.toLocaleString('en-US', { month: 'short' });
  const year = date.getFullYear();
  return `${day} ${month} ${year}`;
}

function getDaysLeft(endDate: string): number {
  const now = new Date();
  const end = new Date(endDate);
  const diff = Math.ceil((end.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
  return diff > 0 ? diff : 0;
}

function getTotalSpent(datas: Budget[]): number {
  return datas.reduce((acc, b) => acc + (b.totalSpent ?? 0), 0);
}

function getEndDate(datas: Budget[]): string {
  if (!datas.length) return '';
  return datas.reduce((max, b) => b.endDate > max ? b.endDate : max, datas[0].endDate);
}

function goToAddBudget() {
  goto('/budgets/create');
}
</script>

<svelte:head>
  <title>Budgets</title>
  <meta name="description" content="Manajemen Budgets" />
</svelte:head>

<div class="budgets">
  {#if loading}
    <LoadingState message="Memuat data budget..." />
  {:else if error}
    <div class="error">{error}</div>
  {:else if budgetGroups.length === 0}
    <div class="budget-summary-graph">
      <div class="budget-summary-amount">Amount you can spend</div>
      <div class="budget-summary-value">{formatCurrency(0)}</div>
      <ProgressBar percent={0} />
      <div class="budget-summary-row">
        <div>
          <div class="budget-summary-label">{formatCurrency(0)}</div>
          <div class="budget-summary-desc">Total budgets</div>
        </div>
        <div>
          <div class="budget-summary-label">{formatCurrency(0)}</div>
          <div class="budget-summary-desc">Total spent</div>
        </div>
        <div>
          <div class="budget-summary-label">0 days</div>
          <div class="budget-summary-desc">End of period</div>
        </div>
      </div>
      <Button className="create-budget-btn" variant="primary-solid" on:click={() => goto('/budgets/create')}>
        Create Budget
      </Button>
    </div>
  {:else}
    
    {#if activeGroup}
      <div class="budget-summary-graph">
        <div class="budget-summary-amount">Amount you can spend</div>
        <div class="budget-summary-value">{formatCurrency(activeGroup?.totalBudget - getTotalSpent(activeGroup?.datas ?? []))}</div>
        <ProgressBar percent={Math.round((getTotalSpent(activeGroup?.datas ?? []) / (activeGroup?.totalBudget ?? 1)) * 100)} />
        <div class="budget-summary-row">
          <div>
            <div class="budget-summary-label">{formatCurrency(activeGroup?.totalBudget ?? 0)}</div>
            <div class="budget-summary-desc">Total budgets</div>
          </div>
          <div>
            <div class="budget-summary-label">{formatCurrency(getTotalSpent(activeGroup?.datas ?? []))}</div>
            <div class="budget-summary-desc">Total spent</div>
          </div>
          <div>
            <div class="budget-summary-label">{getDaysLeft(getEndDate(activeGroup?.datas ?? []))} days</div>
            <div class="budget-summary-desc">End of period</div>
          </div>
        </div>
        <Button variant="primary-solid" on:click={() => goto('/budgets/create')}>
          Create Budget
        </Button>
      </div>
    {/if}
    
    <div class="budget-tabs-scroll">
      <div class="budget-tabs">
        {#each (budgetGroups ?? []) as group}
          <button class:active={activeTab === group.period} on:click={() => activeTab = group.period}>
            {group.label}
          </button>
        {/each}
      </div>
    </div>
    
    {#if activeGroup}
      <Card marginBottom={'16px'} marginTop={'0px'} padding={'0px'} showGradient={true}>
        <div class="budget-group-header">
          <span class="budget-group-title">{activeGroup?.label ?? ''}</span>
          <span class="budget-group-total">Total: {formatCurrency(activeGroup?.totalBudget ?? 0)}</span>
        </div>
        {#each (activeGroup?.datas ?? []) as budget}
          <div class="budget-item-row">
            <CardItem
              iconComponent={IconDisplay}
              icon={budget.icon ?? ''}
              iconProps={{ icon: budget.icon ?? '', alt: 'Budget Icon' }}
              title={budget.name}
              subtitle={'Spent ' + formatCurrency(budget.totalSpent ?? 0)}
              amount={formatCurrency(budget.amount)}
              type="neutral"
              onClick={() => { currentBudget.set(budget); goto('/budgets/create'); }}
            />
            <ProgressBar percent={Math.round((budget.totalSpent ?? 0) / budget.amount * 100)} />
          </div>
        {/each}
      </Card>
    {/if}
  {/if}
  <FloatingButton label="+" handleClick={(link) => { goto('/budgets/create'); return null; }} />
</div>

<style>
.budgets {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}
.error {
  color: red;
  text-align: center;
  margin: 1rem 0;
}

.budget-group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  padding: 4px 0;
}
.budget-group-title {
  font-weight: 600;
  font-size: 1.1rem;
  color: var(--color-theme-1, #00e6b8);
}
.budget-group-total {
  font-size: 0.95rem;
  color: #888;
}
.budget-item-row {
  margin-bottom: 16px;
}
.budget-summary-graph {
  width: 100%;
  max-width: 480px;
  margin: 0 auto 24px auto;
  background: var(--glassy-bg-light);
  border-radius: 20px;
  padding: 32px 16px 24px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 4px 16px var(--glassy-shadow-light), 0 1px 4px rgba(44, 62, 80, 0.08);
}
.budget-summary-amount {
  color: var(--color-text-muted);
  font-size: 1.1rem;
  margin-bottom: 8px;
}
.budget-summary-value {
  color: var(--color-theme-1);
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 18px;
}
.budget-summary-row {
  display: flex;
  width: 100%;
  justify-content: space-between;
  margin-top: 8px;
  margin-bottom: 16px;
}
.budget-summary-label {
  font-size: 1.1rem;
  font-weight: 600;
  text-align: center;
}
.budget-summary-desc {
  font-size: 0.95rem;
  color: var(--color-text-muted);
  text-align: center;
}
.budget-tabs-scroll {
  width: 100%;
  overflow-x: auto;
  margin-bottom: 18px;
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
.budget-tabs-scroll::-webkit-scrollbar {
  display: none;
}
.budget-tabs {
  display: flex;
  gap: 8px;
  justify-content: flex-start;
  min-width: max-content;
  padding-bottom: 2px;
}
.budget-tabs button {
  background: none;
  border: none;
  padding: 8px 18px;
  border-radius: 20px;
  font-size: 1rem;
  font-weight: 500;
  color: var(--color-text-muted);
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  white-space: nowrap;
}
.budget-tabs button.active {
  background: var(--color-theme-1);
  color: var(--color-bg-2);
}

:global(.dark) .budget-summary-graph {
  color: #f3f3f3;
  position: relative;
}
:global(.dark) .budget-summary-graph::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    45deg,
    rgba(255, 255, 255, 0.1) 0%,
    transparent 50%,
    rgba(255, 255, 255, 0.1) 100%
  );
  pointer-events: none;
  border-radius: 20px;
}
:global(.dark) .budget-summary-graph > * {
  position: relative;
  z-index: 1;
}
</style> 