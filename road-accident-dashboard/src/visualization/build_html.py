import json

with open("road-accident-dashboard/outputs/dashboard_data.json", "r", encoding="utf-8") as f:
    data_json = f.read()

html_content = r"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Road Accidents in Thailand 2024 (2567)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Sarabun', sans-serif; background-color: #f3f4f6; }
        .tab-active { border-bottom: 2px solid #3b82f6; color: #3b82f6; font-weight: 600; }
        .tab-inactive { color: #6b7280; }
        .tab-inactive:hover { color: #374151; }
        [v-cloak] { display: none; }
    </style>
</head>
<body>
    <div id="app" v-cloak class="min-h-screen flex flex-col">
        <!-- Header -->
        <header class="bg-blue-900 text-white shadow">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <h1 class="text-3xl font-bold">Road Accidents in Thailand 2024 (2567)</h1>
                <p class="mt-2 text-blue-200">Where, When, Who, and Why? (REAL DATA ONLY)</p>
            </div>
        </header>

        <!-- Filters -->
        <div class="bg-white shadow-sm mb-6 border-b">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                <h2 class="text-lg font-semibold mb-3">Global Filters</h2>
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Month</label>
                        <select v-model="filters.month" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border">
                            <option value="all">All Months</option>
                            <option v-for="m in months" :key="m.value" :value="m.value">{{ m.label }}</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Province</label>
                        <select v-model="filters.province" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border">
                            <option value="all">All Provinces</option>
                            <option v-for="p in availableProvinces" :key="p" :value="p">{{ p }}</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Sex</label>
                        <select v-model="filters.sex" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border">
                            <option value="all">All Genders</option>
                            <option value="ชาย">Male (ชาย)</option>
                            <option value="หญิง">Female (หญิง)</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Age Group</label>
                        <select v-model="filters.age" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2 border">
                            <option value="all">All Ages</option>
                            <option v-for="a in availableAges" :key="a" :value="a">{{ a }}</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>

        <main class="flex-grow max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full mb-10">
            <!-- Navigation -->
            <nav class="flex space-x-8 mb-6 overflow-x-auto border-b border-gray-200">
                <button v-for="tab in tabs" :key="tab.id" @click="currentTab = tab.id" 
                    :class="['pb-4 px-1 text-sm font-medium whitespace-nowrap', currentTab === tab.id ? 'tab-active' : 'tab-inactive']">
                    {{ tab.label }}
                </button>
            </nav>

            <!-- Dashboard Content -->
            <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200 min-h-[500px]">
                
                <!-- Page 1: Overview -->
                <div v-show="currentTab === 'overview'" class="space-y-8">
                    <h2 class="text-2xl font-bold mb-4 border-l-4 border-blue-500 pl-3">Overview</h2>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div class="bg-blue-50 rounded-lg p-6 border border-blue-100 shadow-sm">
                            <h3 class="text-blue-800 text-sm font-bold uppercase tracking-wider mb-2">Total Recorded Deaths</h3>
                            <p class="text-4xl font-extrabold text-blue-900">{{ filteredData.length.toLocaleString() }}</p>
                            <p class="text-xs text-gray-500 mt-2">Verified from open data (rtddi 2567)</p>
                        </div>
                        <div class="bg-orange-50 rounded-lg p-6 border border-orange-100 shadow-sm">
                            <h3 class="text-orange-800 text-sm font-bold uppercase tracking-wider mb-2">Top Affected Province</h3>
                            <p class="text-3xl font-extrabold text-orange-900">{{ topProvince.name }}</p>
                            <p class="text-sm text-gray-600 mt-2">{{ topProvince.count.toLocaleString() }} deaths</p>
                        </div>
                        <div class="bg-red-50 rounded-lg p-6 border border-red-100 shadow-sm">
                            <h3 class="text-red-800 text-sm font-bold uppercase tracking-wider mb-2">Most Involved Vehicle</h3>
                            <p class="text-3xl font-extrabold text-red-900">{{ topVehicle.name }}</p>
                            <p class="text-sm text-gray-600 mt-2">{{ topVehicle.count.toLocaleString() }} deaths</p>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
                        <div>
                            <h3 class="text-lg font-semibold mb-4 text-center">Top 10 Provinces by Deaths</h3>
                            <canvas id="overviewProvChart"></canvas>
                        </div>
                        <div>
                            <h3 class="text-lg font-semibold mb-4 text-center">Deaths by Vehicle Type</h3>
                            <canvas id="overviewVehChart"></canvas>
                        </div>
                    </div>
                </div>

                <!-- Page 2: Where -->
                <div v-show="currentTab === 'where'" class="space-y-8">
                    <h2 class="text-2xl font-bold mb-4 border-l-4 border-blue-500 pl-3">Where? (Location Analysis)</h2>
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                        <div>
                            <h3 class="text-lg font-semibold mb-4 text-center">Provinces with Highest Deaths</h3>
                            <canvas id="whereProvChart"></canvas>
                        </div>
                        <div>
                            <h3 class="text-lg font-semibold mb-4 text-center">Districts with Highest Deaths (Top 15)</h3>
                            <canvas id="whereDistChart"></canvas>
                        </div>
                    </div>
                    <div class="mt-8">
                        <p class="text-sm text-gray-600 italic">* Note: Geographic coordinates were largely missing in the verified open data, so map visualization is unavailable. District and Province names are used instead.</p>
                    </div>
                </div>

                <!-- Page 3: When -->
                <div v-show="currentTab === 'when'" class="space-y-8">
                    <h2 class="text-2xl font-bold mb-4 border-l-4 border-blue-500 pl-3">When? (Time Analysis)</h2>
                    
                    <div v-if="filteredData.length > 0">
                        <h3 class="text-lg font-semibold mb-4 text-center">Deaths by Month (2024 / 2567)</h3>
                        <div class="h-80 relative w-full mb-8">
                            <canvas id="whenMonthChart"></canvas>
                        </div>
                    </div>
                    
                    <div class="p-4 bg-gray-100 rounded-md">
                        <p class="text-sm text-gray-700">
                            <strong>Note on Data Availability:</strong> The open dataset for 2567 only contains the final death date. Time of incident (Time Rec) was completely missing (100% null) in the verified dataset. Therefore, time-of-day analysis cannot be shown without fabricating data.
                        </p>
                    </div>
                </div>

                <!-- Page 4: Who -->
                <div v-show="currentTab === 'who'" class="space-y-8">
                    <h2 class="text-2xl font-bold mb-4 border-l-4 border-blue-500 pl-3">Who? (Demographic Analysis)</h2>
                    
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                        <div>
                            <h3 class="text-lg font-semibold mb-4 text-center">Deaths by Gender</h3>
                            <div class="w-2/3 mx-auto">
                                <canvas id="whoSexChart"></canvas>
                            </div>
                        </div>
                        <div>
                            <h3 class="text-lg font-semibold mb-4 text-center">Deaths by Age Group</h3>
                            <canvas id="whoAgeChart"></canvas>
                        </div>
                    </div>
                </div>

                <!-- Page 5: Why -->
                <div v-show="currentTab === 'why'" class="space-y-8">
                    <h2 class="text-2xl font-bold mb-4 border-l-4 border-blue-500 pl-3">Why? (Vehicles & Causes)</h2>
                    
                    <div>
                        <h3 class="text-lg font-semibold mb-4 text-center">Vehicles Involved in Fatalities</h3>
                        <canvas id="whyVehChart"></canvas>
                    </div>
                    
                    <div class="p-4 bg-gray-100 rounded-md mt-6">
                        <p class="text-sm text-gray-700">
                            <strong>Note on Causes:</strong> Specific accident causes (e.g., speeding, drunk driving) and road characteristics are not present in this mortality dataset (rtddi 3 bases). 
                            The dataset focuses on mortality count, vehicle type, and location. We only display what is verifiable.
                        </p>
                    </div>
                </div>

                <!-- Page 6: Insights -->
                <div v-show="currentTab === 'insights'" class="space-y-6">
                    <h2 class="text-2xl font-bold mb-4 border-l-4 border-blue-500 pl-3">Management Insights</h2>
                    
                    <div v-if="filteredData.length === 0" class="text-gray-500">No data available for the current filters.</div>
                    
                    <div v-else class="space-y-4">
                        <div class="p-5 bg-white border border-gray-200 rounded-lg shadow-sm">
                            <h4 class="font-bold text-gray-900 text-lg mb-2">1. Priority Areas (Where)</h4>
                            <p class="text-gray-700">The province with the highest number of fatalities is <strong>{{ topProvince.name }}</strong> with {{ topProvince.count.toLocaleString() }} deaths. District-level attention should focus on <strong>{{ topDistrict.name }}</strong> ({{ topDistrict.count }} deaths). These areas should receive immediate road safety interventions and resource allocation.</p>
                        </div>

                        <div class="p-5 bg-white border border-gray-200 rounded-lg shadow-sm">
                            <h4 class="font-bold text-gray-900 text-lg mb-2">2. Most Vulnerable Groups (Who)</h4>
                            <p class="text-gray-700">The demographic most affected based on the verified data is <strong>{{ topSex.name }}</strong> ({{ ((topSex.count / filteredData.length) * 100).toFixed(1) }}% of deaths), particularly in the age group <strong>{{ topAge.name }}</strong>. Targeted awareness campaigns should be designed for this demographic.</p>
                        </div>

                        <div class="p-5 bg-white border border-gray-200 rounded-lg shadow-sm">
                            <h4 class="font-bold text-gray-900 text-lg mb-2">3. Vehicle Risk Factors (Why)</h4>
                            <p class="text-gray-700"><strong>{{ topVehicle.name }}</strong> are involved in the vast majority of fatal accidents ({{ topVehicle.count }} deaths). Note that 'ไม่ระบุพาหนะ' (Unspecified vehicle) accounts for a large portion, indicating a need for better data collection at the scene.</p>
                        </div>
                        
                        <div class="p-5 bg-white border border-gray-200 rounded-lg shadow-sm">
                            <h4 class="font-bold text-gray-900 text-lg mb-2">4. Temporal Patterns (When)</h4>
                            <p class="text-gray-700">The month with the highest recorded deaths is <strong>{{ months.find(m => m.value == topMonth.name)?.label || topMonth.name }}</strong> ({{ topMonth.count }} deaths). Law enforcement and emergency services should be on higher alert during this period.</p>
                        </div>
                    </div>
                </div>

                <!-- Page 7: Data Sources -->
                <div v-show="currentTab === 'sources'" class="space-y-6">
                    <h2 class="text-2xl font-bold mb-4 border-l-4 border-blue-500 pl-3">Data Sources & Traceability</h2>
                    
                    <div class="bg-gray-50 p-6 rounded-lg border border-gray-200">
                        <h3 class="text-lg font-bold mb-4">Verified Open Data Source</h3>
                        <table class="w-full text-sm text-left text-gray-700">
                            <tbody>
                                <tr class="border-b border-gray-200"><th class="py-2 pr-4 font-semibold w-1/3">Dataset Name</th><td class="py-2">ข้อมูลผู้เสียชีวิตจากอุบัติเหตุทางถนน จากระบบบูรณาการข้อมูลการตายจากอุบัติเหตุทางถนน (3 ฐาน) ปี 2567</td></tr>
                                <tr class="border-b border-gray-200"><th class="py-2 pr-4 font-semibold">Organization</th><td class="py-2">กรมควบคุมโรค (Department of Disease Control)</td></tr>
                                <tr class="border-b border-gray-200"><th class="py-2 pr-4 font-semibold">Source URL</th><td class="py-2"><a href="https://data.go.th/dataset/rtddi" target="_blank" class="text-blue-600 hover:underline">https://data.go.th/dataset/rtddi</a></td></tr>
                                <tr class="border-b border-gray-200"><th class="py-2 pr-4 font-semibold">Data Period</th><td class="py-2">2024 (2567)</td></tr>
                                <tr class="border-b border-gray-200"><th class="py-2 pr-4 font-semibold">Total Verified Rows</th><td class="py-2">17,477</td></tr>
                                <tr><th class="py-2 pr-4 font-semibold">Verification Status</th><td class="py-2 text-green-600 font-bold">VERIFIED REAL DATA</td></tr>
                            </tbody>
                        </table>
                    </div>
                    
                    <div class="bg-gray-50 p-6 rounded-lg border border-gray-200 mt-6">
                        <h3 class="text-lg font-bold mb-4">Traceability Log (KPIs & Metrics)</h3>
                        <ul class="space-y-4 text-sm text-gray-700">
                            <li><strong>Total Deaths:</strong> <code>COUNT(*)</code> of rows in the dataset for 2567.</li>
                            <li><strong>Deaths by Province:</strong> <code>GROUP BY จ.ที่เสียชีวิต (Accident Province)</code>.</li>
                            <li><strong>Deaths by Age Group:</strong> Derived from <code>Age</code> column (binned into groups). Records with missing age are marked "ไม่ระบุ".</li>
                            <li><strong>Deaths by Vehicle Type:</strong> <code>GROUP BY vehicle_merge_final</code>.</li>
                            <li><strong>Deaths by Date/Month:</strong> Extracted from <code>dead_date_final</code> column. Missing month values are excluded from the trend chart.</li>
                        </ul>
                        <div class="mt-4 p-3 bg-yellow-50 border-l-4 border-yellow-400">
                            <p class="text-xs text-yellow-800"><strong>Strict Data Policy Enforced:</strong> No data imputation, fabrication, or random values were used. Fields not present in the verified open data (such as accident causes, accident coordinates, time of day) are strictly omitted from visualizations.</p>
                        </div>
                    </div>
                </div>

            </div>
        </main>
    </div>

    <script>
        const rawData = {{DATA_JSON_PLACEHOLDER}};

        const { createApp } = Vue;

        let charts = {};

        createApp({
            data() {
                return {
                    data: rawData,
                    tabs: [
                        { id: 'overview', label: 'Overview' },
                        { id: 'where', label: 'Where?' },
                        { id: 'when', label: 'When?' },
                        { id: 'who', label: 'Who?' },
                        { id: 'why', label: 'Why?' },
                        { id: 'insights', label: 'Management Insights' },
                        { id: 'sources', label: 'Data Sources' },
                    ],
                    currentTab: 'overview',
                    filters: {
                        month: 'all',
                        province: 'all',
                        sex: 'all',
                        age: 'all'
                    },
                    months: [
                        { value: 1, label: 'January' }, { value: 2, label: 'February' }, { value: 3, label: 'March' },
                        { value: 4, label: 'April' }, { value: 5, label: 'May' }, { value: 6, label: 'June' },
                        { value: 7, label: 'July' }, { value: 8, label: 'August' }, { value: 9, label: 'September' },
                        { value: 10, label: 'October' }, { value: 11, label: 'November' }, { value: 12, label: 'December' }
                    ]
                }
            },
            computed: {
                availableProvinces() {
                    return [...new Set(this.data.map(d => d.province))].sort();
                },
                availableAges() {
                    return [...new Set(this.data.map(d => d.age_group))].sort();
                },
                filteredData() {
                    return this.data.filter(d => {
                        let match = true;
                        if (this.filters.month !== 'all') match = match && d.month === parseInt(this.filters.month);
                        if (this.filters.province !== 'all') match = match && d.province === this.filters.province;
                        if (this.filters.sex !== 'all') match = match && d.sex === this.filters.sex;
                        if (this.filters.age !== 'all') match = match && d.age_group === this.filters.age;
                        return match;
                    });
                },
                topProvince() {
                    return this.getTopN(this.filteredData, 'province', 1)[0] || { name: 'N/A', count: 0 };
                },
                topDistrict() {
                    const withDist = this.filteredData.filter(d => d.district !== 'ไม่ระบุ');
                    return this.getTopN(withDist, 'district', 1)[0] || { name: 'N/A', count: 0 };
                },
                topVehicle() {
                    return this.getTopN(this.filteredData, 'vehicle', 1)[0] || { name: 'N/A', count: 0 };
                },
                topSex() {
                    return this.getTopN(this.filteredData, 'sex', 1)[0] || { name: 'N/A', count: 0 };
                },
                topAge() {
                    return this.getTopN(this.filteredData, 'age_group', 1)[0] || { name: 'N/A', count: 0 };
                },
                topMonth() {
                    return this.getTopN(this.filteredData.filter(d => d.month > 0), 'month', 1)[0] || { name: 'N/A', count: 0 };
                }
            },
            methods: {
                getTopN(data, key, n) {
                    const counts = {};
                    data.forEach(d => {
                        counts[d[key]] = (counts[d[key]] || 0) + 1;
                    });
                    const sorted = Object.keys(counts).map(k => ({ name: k, count: counts[k] })).sort((a, b) => b.count - a.count);
                    return sorted.slice(0, n);
                },
                updateCharts() {
                    const data = this.filteredData;
                    
                    const renderBarChart = (canvasId, key, limit = 10, label = 'Deaths') => {
                        const topData = this.getTopN(data, key, limit);
                        const ctx = document.getElementById(canvasId);
                        if (!ctx) return;
                        
                        if (charts[canvasId]) charts[canvasId].destroy();
                        
                        charts[canvasId] = new Chart(ctx, {
                            type: 'bar',
                            data: {
                                labels: topData.map(d => d.name),
                                datasets: [{
                                    label: label,
                                    data: topData.map(d => d.count),
                                    backgroundColor: '#3b82f6'
                                }]
                            },
                            options: {
                                responsive: true,
                                indexAxis: 'y'
                            }
                        });
                    };

                    const renderPieChart = (canvasId, key) => {
                        const topData = this.getTopN(data, key, 10);
                        const ctx = document.getElementById(canvasId);
                        if (!ctx) return;
                        
                        if (charts[canvasId]) charts[canvasId].destroy();
                        
                        charts[canvasId] = new Chart(ctx, {
                            type: 'doughnut',
                            data: {
                                labels: topData.map(d => d.name),
                                datasets: [{
                                    data: topData.map(d => d.count),
                                    backgroundColor: ['#3b82f6', '#ef4444', '#f59e0b', '#10b981', '#6366f1', '#8b5cf6', '#ec4899', '#14b8a6']
                                }]
                            },
                            options: { responsive: true }
                        });
                    };

                    const renderLineChart = (canvasId) => {
                        const ctx = document.getElementById(canvasId);
                        if (!ctx) return;
                        
                        const counts = {};
                        for (let i = 1; i <= 12; i++) counts[i] = 0;
                        
                        data.forEach(d => {
                            if (d.month > 0) counts[d.month] = (counts[d.month] || 0) + 1;
                        });
                        
                        const monthlyData = Object.values(counts);
                        const monthLabels = this.months.map(m => m.label);
                        
                        if (charts[canvasId]) charts[canvasId].destroy();
                        
                        charts[canvasId] = new Chart(ctx, {
                            type: 'line',
                            data: {
                                labels: monthLabels,
                                datasets: [{
                                    label: 'Deaths',
                                    data: monthlyData,
                                    borderColor: '#ef4444',
                                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                                    fill: true,
                                    tension: 0.3
                                }]
                            },
                            options: {
                                responsive: true,
                                maintainAspectRatio: false
                            }
                        });
                    };

                    if (this.currentTab === 'overview') {
                        renderBarChart('overviewProvChart', 'province', 10);
                        renderPieChart('overviewVehChart', 'vehicle');
                    } else if (this.currentTab === 'where') {
                        renderBarChart('whereProvChart', 'province', 15);
                        renderBarChart('whereDistChart', 'district', 15);
                    } else if (this.currentTab === 'when') {
                        renderLineChart('whenMonthChart');
                    } else if (this.currentTab === 'who') {
                        renderPieChart('whoSexChart', 'sex');
                        renderBarChart('whoAgeChart', 'age_group', 10, 'Deaths');
                    } else if (this.currentTab === 'why') {
                        renderBarChart('whyVehChart', 'vehicle', 15);
                    }
                }
            },
            watch: {
                filteredData() {
                    this.$nextTick(() => {
                        this.updateCharts();
                    });
                },
                currentTab() {
                    this.$nextTick(() => {
                        this.updateCharts();
                    });
                }
            },
            mounted() {
                this.updateCharts();
            }
        }).mount('#app');
    </script>
</body>
</html>
"""

html_content = html_content.replace("{{DATA_JSON_PLACEHOLDER}}", data_json)

with open("road-accident-dashboard/outputs/road_accident_dashboard.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Dashboard built successfully at road-accident-dashboard/outputs/road_accident_dashboard.html")
