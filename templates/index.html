{% extends "base.html" %}

{% block content %}
<div class="mb-4">
    <h1 class="text-2xl font-bold tracking-tight">Relative Strength Dashboard</h1>
    <p class="text-sm text-gray-500">
        vs SPY · Abs / Rel / Percentile · Last update: {{ last_update }}
    </p>
</div>

<div class="flex gap-2 overflow-x-auto pb-3 mb-4">
    <a href="/?group=screening"
       class="px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap
              {% if active_group == 'screening' %}bg-blue-600 text-white{% else %}bg-white border border-gray-200{% endif %}">
        Screening
    </a>
    <a href="/?group=movers"
       class="px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap
              {% if active_group == 'movers' %}bg-blue-600 text-white{% else %}bg-white border border-gray-200{% endif %}">
        Movers
    </a>
    <a href="/?group=sectors&sort=rel_1m&dir=desc"
       class="px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap
              {% if active_group == 'sectors' %}bg-blue-600 text-white{% else %}bg-white border border-gray-200{% endif %}">
        Sectors
    </a>
    <a href="/?group=countries&sort=rel_1m&dir=desc"
       class="px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap
              {% if active_group == 'countries' %}bg-blue-600 text-white{% else %}bg-white border border-gray-200{% endif %}">
        Countries
    </a>
    <a href="/?group=equal_weight&sort=rel_1m&dir=desc"
       class="px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap
              {% if active_group == 'equal_weight' %}bg-blue-600 text-white{% else %}bg-white border border-gray-200{% endif %}">
        Equal Weight
    </a>
    <a href="/?group=all&sort=rel_1m&dir=desc"
       class="px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap
              {% if active_group == 'all' %}bg-blue-600 text-white{% else %}bg-white border border-gray-200{% endif %}">
        All
    </a>
</div>

{% macro sort_link(col, label) -%}
    {% set next_dir = 'asc' if sort == col and dir == 'desc' else 'desc' %}
    <a href="/?group={{ active_group }}&sort={{ col }}&dir={{ next_dir }}"
       class="inline-flex items-center gap-1 hover:text-blue-600 whitespace-nowrap">
        {{ label }}
        {% if sort == col %}
            <span class="text-blue-600">{{ '▼' if dir == 'desc' else '▲' }}</span>
        {% endif %}
    </a>
{%- endmacro %}

{% macro pct_cell(val) -%}
    {% if val is none %}
        <span class="text-gray-300">–</span>
    {% else %}
        <span class="{% if val > 0 %}text-green-600{% elif val < 0 %}text-red-600{% else %}text-gray-700{% endif %} font-medium">
            {{ "%+.2f"|format(val) }}%
        </span>
    {% endif %}
{%- endmacro %}

{% macro num_cell(val, digits=0) -%}
    {% if val is none %}
        <span class="text-gray-300">–</span>
    {% else %}
        {{ "%.0f"|format(val) if digits == 0 else ("%.2f"|format(val)) }}
    {% endif %}
{%- endmacro %}

{% macro heat_cell(val, extra='') -%}
    {% if val is none %}
        <td class="px-2 py-2.5 text-right {{ extra }}">
            <span class="text-gray-300">–</span>
        </td>
    {% else %}
        {% set hue = (val * 1.2)|round|int %}
        <td class="px-2 py-2.5 text-right font-medium {{ extra }}"
            style="background-color: hsl({{ hue }}, 58%, 94%); color: hsl({{ hue }}, 48%, 28%);">
            {{ "%.0f"|format(val) }}
        </td>
    {% endif %}
{%- endmacro %}

{% macro rs_table(rows, show_sort=True) %}
<div class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100">
    <div class="table-scroll">
        <table class="rs-table w-full text-sm">
            <thead class="bg-gray-50 text-left text-xs uppercase tracking-wide text-gray-500">
                <tr>
                   <th class="px-3 py-3 font-semibold col-sticky">
                        {% if show_sort %}{{ sort_link('ticker', 'Ticker') }}{% else %}Ticker{% endif %}
                    </th>
                    <th class="px-3 py-3 font-semibold">
                        {% if show_sort %}{{ sort_link('name', 'Name') }}{% else %}Name{% endif %}
                    </th>
                    <th class="px-2 py-3 font-semibold text-right border-l border-gray-200">
                        {% if show_sort %}{{ sort_link('abs_1w', 'Abs 1W') }}{% else %}Abs 1W{% endif %}
                    </th>
                    <th class="px-2 py-3 font-semibold text-right">
                        {% if show_sort %}{{ sort_link('abs_1m', 'Abs 1M') }}{% else %}Abs 1M{% endif %}
                    </th>
                    <th class="px-2 py-3 font-semibold text-right">
                        {% if show_sort %}{{ sort_link('abs_3m', 'Abs 3M') }}{% else %}Abs 3M{% endif %}
                    </th>
                    <th class="px-2 py-3 font-semibold text-right">
                        {% if show_sort %}{{ sort_link('abs_1y', 'Abs 1Y') }}{% else %}Abs 1Y{% endif %}
                    </th>
                    <th class="px-2 py-3 font-semibold text-right">
                        {% if show_sort %}{{ sort_link('abs_ytd', 'Abs YTD') }}{% else %}Abs YTD{% endif %}
                    </th>
                    <th class="px-2 py-3 font-semibold text-right border-l border-gray-200">
                        {% if show_sort %}{{ sort_link('rel_1w', 'Rel 1W') }}{% else %}Rel 1W{% endif %}
                    </th>
                    <th class="px-2 py-3 font-semibold text-right bg-blue-50">
                        {% if show_sort %}{{ sort_link('rel_1m', 'Rel 1M') }}{% else %}Rel 1M{% endif %}
                    </th>
                    <th class="px-2 py-3 font-semibold text-right bg-amber-50">
                        {% if show_sort %}{{ sort_link('rel_1m_chg', 'Δ Rel 1M') }}{% else %}Δ Rel 1M{% endif %}
                    </th>
                    <th class="px-2 py-3 font-semibold text-right">
                        {% if show_sort %}{{ sort_link('rel_3m', 'Rel 3M') }}{% else %}Rel 3M{% endif %}
                    </th>
                    <th class="px-2 py-3 font-semibold text-right">
                        {% if show_sort %}{{ sort_link('rel_1y', 'Rel 1Y') }}{% else %}Rel 1Y{% endif %}
                    </th>
                    <th class="px-2 py-3 font-semibold text-right">
                        {% if show_sort %}{{ sort_link('rel_ytd', 'Rel YTD') }}{% else %}Rel YTD{% endif %}
                    </th>
                    <th class="px-2 py-3 font-semibold text-right border-l border-gray-200">
                        {% if show_sort %}{{ sort_link('pct_1w', 'Pct 1W') }}{% else %}Pct 1W{% endif %}
                    </th>
                    <th class="px-2 py-3 font-semibold text-right">
                        {% if show_sort %}{{ sort_link('pct_1m', 'Pct 1M') }}{% else %}Pct 1M{% endif %}
                    </th>
                    <th class="px-2 py-3 font-semibold text-right">
                        {% if show_sort %}{{ sort_link('pct_3m', 'Pct 3M') }}{% else %}Pct 3M{% endif %}
                    </th>
                    <th class="px-2 py-3 font-semibold text-right">
                        {% if show_sort %}{{ sort_link('pct_1y', 'Pct 1Y') }}{% else %}Pct 1Y{% endif %}
                    </th>
                    <th class="px-2 py-3 font-semibold text-right">
                        {% if show_sort %}{{ sort_link('pct_ytd', 'Pct YTD') }}{% else %}Pct YTD{% endif %}
                    </th>
                    <th class="px-3 py-3 font-semibold border-l border-gray-200 min-w-[7rem]">1M RS</th>
                    <th class="px-3 py-3 font-semibold border-l border-gray-200 min-w-[10rem]">6M RS</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
                {% for item in rows %}
                <tr class="hover:bg-gray-50/80">
                    <td class="px-3 py-2.5 font-semibold col-sticky">
                        <a href="https://elite.finviz.com/stock?t={{ item.ticker }}&p=d"
                           target="_blank"
                           rel="noopener noreferrer"
                           class="text-blue-700 hover:underline">
                            {{ item.ticker }}
                        </a>
                    </td>
                    <td class="px-3 py-2.5 text-gray-600 whitespace-nowrap">
                        <a href="https://elite.finviz.com/screener?v=211&p=d&f=etf_heldby_{{ item.ticker }}&ft=5&ta=0&o=-perf52w"
                           target="_blank"
                           rel="noopener noreferrer"
                           class="text-gray-700 hover:text-blue-700 hover:underline">
                            {{ item.name }}
                        </a>
                    </td>
                    <td class="px-2 py-2.5 text-right border-l border-gray-100">{{ pct_cell(item.abs_1w) }}</td>
                    <td class="px-2 py-2.5 text-right">{{ pct_cell(item.abs_1m) }}</td>
                    <td class="px-2 py-2.5 text-right">{{ pct_cell(item.abs_3m) }}</td>
                    <td class="px-2 py-2.5 text-right">{{ pct_cell(item.abs_1y) }}</td>
                    <td class="px-2 py-2.5 text-right">{{ pct_cell(item.abs_ytd) }}</td>
                    <td class="px-2 py-2.5 text-right border-l border-gray-100">{{ pct_cell(item.rel_1w) }}</td>
                    <td class="px-2 py-2.5 text-right bg-blue-50/40 font-semibold">{{ pct_cell(item.rel_1m) }}</td>
                    <td class="px-2 py-2.5 text-right bg-amber-50/40 font-semibold">{{ pct_cell(item.rel_1m_chg) }}</td>
                    <td class="px-2 py-2.5 text-right">{{ pct_cell(item.rel_3m) }}</td>
                    <td class="px-2 py-2.5 text-right">{{ pct_cell(item.rel_1y) }}</td>
                    <td class="px-2 py-2.5 text-right">{{ pct_cell(item.rel_ytd) }}</td>
                    {{ heat_cell(item.pct_1w, 'border-l border-gray-100') }}
                    {{ heat_cell(item.pct_1m) }}
                    {{ heat_cell(item.pct_3m) }}
                    {{ heat_cell(item.pct_1y) }}
                    {{ heat_cell(item.pct_ytd) }}
                    <td class="px-3 py-2.5 border-l border-gray-100 min-w-[7rem]">
                        {% if item.sparkline and item.sparkline|length > 1 %}
                        <svg class="h-6 w-28 block" viewBox="0 0 100 24" preserveAspectRatio="none">
                            <polyline
                                fill="none"
                                stroke="{% if item.rel_1m is not none and item.rel_1m >= 0 %}#16a34a{% else %}#dc2626{% endif %}"
                                stroke-width="2"
                                stroke-linejoin="round"
                                stroke-linecap="round"
                                points="{% for i in range(item.sparkline|length) %}{{ '%.1f'|format(i / (item.sparkline|length - 1) * 100) }},{{ '%.1f'|format(24 - item.sparkline[i] / 100 * 22) }}{% if not loop.last %} {% endif %}{% endfor %}"
                            />
                        </svg>
                        {% else %}
                        <span class="text-gray-300 text-xs">–</span>
                        {% endif %}
                    </td>
                    <td class="px-3 py-2.5 border-l border-gray-100">
                        {% if item.rs_bars and item.rs_bars|length > 1 %}
                        <svg class="h-7 w-36 block"
                             viewBox="0 0 {{ item.rs_bar_width }} {{ item.rs_bar_height }}"
                             preserveAspectRatio="none"
                             role="img"
                             aria-label="6M chart of 1M relative strength">
                            <line
                                x1="0"
                                y1="{{ item.rs_bar_height / 2 }}"
                                x2="{{ item.rs_bar_width }}"
                                y2="{{ item.rs_bar_height / 2 }}"
                                stroke="#d1d5db"
                                stroke-width="0.6"
                            />
                            {% for bar in item.rs_bars %}
                            <rect
                                x="{{ bar.x }}"
                                y="{{ bar.y }}"
                                width="{{ bar.w }}"
                                height="{{ bar.h }}"
                                fill="{% if bar.up %}#16a34a{% else %}#dc2626{% endif %}"
                            >
                                <title>RS {{ '%.3f'|format(bar.v) }}</title>
                            </rect>
                            {% endfor %}
                        </svg>
                        {% else %}
                        <span class="text-gray-300 text-xs">–</span>
                        {% endif %}
                    </td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="20" class="px-4 py-8 text-center text-gray-400">
                        Keine Daten geladen.
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endmacro %}

{% if active_group == 'screening' %}
<div class="mb-4 flex flex-wrap items-center gap-3">
    {% if screener_url %}
    <a href="{{ screener_url }}"
       target="_blank"
       rel="noopener noreferrer"
       class="inline-flex items-center px-4 py-2 rounded-lg bg-blue-600 text-white text-sm font-medium hover:bg-blue-700">
        Zum Screener
    </a>
    <span class="text-sm text-gray-500">{{ screening_count }} Ticker ohne Duplikate</span>
    {% else %}
    <span class="inline-flex items-center px-4 py-2 rounded-lg bg-gray-200 text-gray-500 text-sm font-medium">
        Zum Screener
    </span>
    <span class="text-sm text-gray-500">Keine Ticker geladen</span>
    {% endif %}
</div>
{% if screening_errors %}
<p class="mb-3 text-xs text-amber-700">{{ screening_errors|join(" · ") }}</p>
{% endif %}
<div class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100">
    <div class="table-scroll">
        <table class="w-full text-sm" style="min-width: 520px;">
            <thead class="bg-gray-50 text-left text-xs uppercase tracking-wide text-gray-500">
                <tr>
                    <th class="px-3 py-3 font-semibold">Ticker</th>
                    <th class="px-3 py-3 font-semibold text-right">
                        {% if header_urls.jahr %}<a href="{{ header_urls.jahr }}" target="_blank" rel="noopener noreferrer" class="hover:text-blue-600 hover:underline">Jahr</a>{% else %}Jahr{% endif %}
                    </th>
                    <th class="px-3 py-3 font-semibold text-right">
                        {% if header_urls.quartal %}<a href="{{ header_urls.quartal }}" target="_blank" rel="noopener noreferrer" class="hover:text-blue-600 hover:underline">Quartal</a>{% else %}Quartal{% endif %}
                    </th>
                    <th class="px-3 py-3 font-semibold text-right">
                        {% if header_urls.monat %}<a href="{{ header_urls.monat }}" target="_blank" rel="noopener noreferrer" class="hover:text-blue-600 hover:underline">Monat</a>{% else %}Monat{% endif %}
                    </th>
                    <th class="px-3 py-3 font-semibold text-right">
                        {% if header_urls.woche %}<a href="{{ header_urls.woche }}" target="_blank" rel="noopener noreferrer" class="hover:text-blue-600 hover:underline">Woche</a>{% else %}Woche{% endif %}
                    </th>
                    <th class="px-3 py-3 font-semibold text-right">
                        {% if header_urls.volume %}<a href="{{ header_urls.volume }}" target="_blank" rel="noopener noreferrer" class="hover:text-blue-600 hover:underline">Volume</a>{% else %}Volume{% endif %}
                    </th>
                    <th class="px-3 py-3 font-semibold text-right">Total</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
                {% for row in screening_rows %}
                <tr class="hover:bg-gray-50/80">
                    <td class="px-3 py-2.5 font-semibold">
                        <a href="https://elite.finviz.com/quote.ashx?t={{ row.ticker }}"
                           target="_blank"
                           rel="noopener noreferrer"
                           class="text-blue-700 hover:underline">{{ row.ticker }}</a>
                    </td>
                    <td class="px-3 py-2.5 text-right">{{ row.jahr }}</td>
                    <td class="px-3 py-2.5 text-right">{{ row.quartal }}</td>
                    <td class="px-3 py-2.5 text-right">{{ row.monat }}</td>
                    <td class="px-3 py-2.5 text-right">{{ row.woche }}</td>
                    <td class="px-3 py-2.5 text-right">{{ row.volume }}</td>
                    <td class="px-3 py-2.5 text-right font-semibold">{{ row.total }}</td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="7" class="px-4 py-8 text-center text-gray-400">
                        Keine Screening-Daten. URLs in data/screeners.py setzen und FINVIZ_API_KEY in Railway.
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% elif active_group == 'movers' %}
<div class="mb-8">
    <h2 class="text-lg font-semibold mb-3">Top 5 Movers · Δ Rel 1M</h2>
    {{ rs_table(movers_top5, show_sort=True) }}
</div>
<div class="mb-8">
    <h2 class="text-lg font-semibold mb-3">Industry Top 10</h2>
    {{ rs_table(movers_industry, show_sort=True) }}
</div>
<div class="mb-8">
    <h2 class="text-lg font-semibold mb-3">Country Top 10</h2>
    {{ rs_table(movers_countries, show_sort=True) }}
</div>
{% else %}
{{ rs_table(data, show_sort=True) }}
{% endif %}

<p class="mt-3 text-xs text-gray-400">
    Ticker → Finviz Stock · Name → Finviz Holdings sortiert nach 52W ·
    Rel = vs SPY · Δ Rel 1M = Rel 1M heute minus Rel 1M vor 1 Monat ·
    Pct = Perzentil im Universum (Heatmap 0 rot → 100 grün) ·
    6M RS = rollierende 1M-RS-Ratio der letzten ~6 Monate
    (grün = Ratio ≥ 1 vs SPY, rot = Ratio &lt; 1)
</p>
{% endblock %}