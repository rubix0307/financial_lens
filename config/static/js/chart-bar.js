// Data configuration block
const data = {
    baseCurrency: 'USD',
    labels: ['Январь', 'Февраль'],
    datasets: [
        {
            name: 'Продукты',
            label: 'Продукты',
            currencies: {
                'Январь': {
                    'GBP': 200,
                    'UAH': 120
                },
                'Февраль': {
                    'USD': 156,
                    'UAH': 890,
                    'EUR': 100,
                    'JPY': 5000
                }
            },
            data: [470.10, 650.00],
            backgroundColor: 'rgba(54, 162, 235, 0.6)',
            hoverBackgroundColor: 'rgba(54, 162, 235, 0.8)',
        },
        {
            name: 'Мебель',
            label: 'Мебель',
            currencies: {
                'Январь': {
                    'USD': 400,
                    'EUR': 100
                }
            },
            data: [405.60, null],
            backgroundColor: 'rgba(153, 102, 255, 0.6)',
            hoverBackgroundColor: 'rgba(153, 102, 255, 0.8)',
        },
        {
            name: 'Электроника',
            label: 'Электроника',
            currencies: {
                'Февраль': {
                    'EUR': 321,
                    'UAH': 98
                }
            },
            data: [null, 351.38],
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            hoverBackgroundColor: 'rgba(75, 192, 192, 0.8)',
        }
    ]
};

// Tooltip footer calculation block
const footer = (tooltipItems) => {
    let sum = 0;
    tooltipItems.forEach(function(tooltipItem) {
        sum += tooltipItem.parsed.y;
    });
    return 'Всего: ' + sum;
};

// Tooltip creation block
const getOrCreateTooltip = (chart) => {
    let tooltipEl = chart.canvas.parentNode.querySelector('div');

    if (!tooltipEl) {
        tooltipEl = document.createElement('div');
        tooltipEl.style.background = 'rgba(0, 0, 0, 0.7)';
        tooltipEl.style.borderRadius = '3px';
        tooltipEl.style.color = 'white';
        tooltipEl.style.opacity = 1;
        tooltipEl.style.pointerEvents = 'none';
        tooltipEl.style.position = 'absolute';
        tooltipEl.style.transform = 'translate(-50%, 0)';

        const table = document.createElement('table');
        table.style.margin = '0px';

        tooltipEl.appendChild(table);
        chart.canvas.parentNode.appendChild(tooltipEl);
    }

    return tooltipEl;
};

// Tooltip handler block
const externalTooltipHandler = (context) => {
    const {chart, tooltip} = context;
    const tooltipEl = getOrCreateTooltip(chart);

    if (tooltip.opacity === 0) {
        tooltipEl.style.opacity = 0;
        return;
    }

    if (tooltip.body) {
        const titleLines = tooltip.title || [];
        const dataset = chart.data.datasets[tooltip.dataPoints[0].datasetIndex];
        const month = tooltip.title[0];
        const currencies = dataset.currencies[month] || {};
        const currenciesInfo = Object.entries(currencies).map(([currency, value]) => `${currency}: ${value}`).join('<br>');
        const tableHead = document.createElement('thead');

        // Header with category name and total sum
        const colorSpan = document.createElement('span');
        colorSpan.style.background = dataset.backgroundColor;
        colorSpan.style.borderRadius = '50%';
        colorSpan.style.display = 'inline-block';
        colorSpan.style.height = '10px';
        colorSpan.style.width = '10px';
        colorSpan.style.marginRight = '5px';

        titleLines.forEach(title => {
            const tr = document.createElement('tr');
            tr.style.borderWidth = 0;

            const th = document.createElement('th');
            th.style.borderWidth = 0;
            th.appendChild(colorSpan.cloneNode(true));
            const totalSum = chart.data.datasets.reduce((sum, dataset) => sum + (dataset.data[tooltip.dataPoints[0].dataIndex] || 0), 0);
            const text = document.createTextNode(`${title}`);
            const br = document.createElement('br');
            const sumText = document.createTextNode(`${totalSum} ${chart.data.baseCurrency}`);

            th.appendChild(text);
            th.appendChild(br);
            th.appendChild(sumText);

            tr.appendChild(th);
            tableHead.appendChild(tr);
        });

        const tableBody = document.createElement('tbody');

        // Footer with category name and individual sum
        const footerTr = document.createElement('tr');
        footerTr.style.borderWidth = 0;
        const footerTd = document.createElement('td');
        footerTd.style.borderWidth = 0;
        footerTd.style.fontWeight = 'bold';
        footerTd.style.paddingTop = '15px';
        footerTd.style.paddingBottom = '15px';

                footerTd.appendChild(document.createTextNode(`${dataset.label}`));

        const footerBr = document.createElement('br');
        const footerSumText = document.createTextNode(`${tooltip.dataPoints[0].parsed.y} ${chart.data.baseCurrency}`);
        footerTd.appendChild(footerBr);
        footerTd.appendChild(footerSumText);
        footerTr.appendChild(footerTd);
        tableBody.appendChild(footerTr);

        // Body with currency details
        const tr = document.createElement('tr');
        tr.style.borderWidth = 0;

        const td = document.createElement('td');
        td.style.borderWidth = 0;
        td.innerHTML = `<div style='color: white; font-weight: bold;'>${currenciesInfo}</div>`;

        tr.appendChild(td);
        tableBody.appendChild(tr);

        const tableRoot = tooltipEl.querySelector('table');

        while (tableRoot.firstChild) {
            tableRoot.firstChild.remove();
        }

        tableRoot.appendChild(tableHead);
        tableRoot.appendChild(tableBody);
    }

    const {offsetLeft: positionX, offsetTop: positionY} = chart.canvas;

    tooltipEl.style.opacity = 1;
    tooltipEl.style.left = positionX + tooltip.caretX + 'px';
    tooltipEl.style.top = positionY + tooltip.caretY + 'px';
    tooltipEl.style.font = tooltip.options.bodyFont.string;
    tooltipEl.style.padding = tooltip.options.padding + 'px ' + tooltip.options.padding + 'px';
};

// Chart configuration block
const config = {
    type: 'bar',
    data: data,
    options: {
        plugins: {
            tooltip: {
                enabled: false,
                position: 'nearest',
                external: externalTooltipHandler
            },
            title: {
                display: true,
                text: 'Stacked Bar Chart with Segment Data on Hover'
            }
        },
        responsive: true,
        scales: {
            x: {
                stacked: true,
            },
            y: {
                stacked: true,
            }
        }
    }
};

// Initialization block
window.onload = function() {
    const ctx = document.getElementById('stackedBarChart').getContext('2d');
    new Chart(ctx, config);
};
