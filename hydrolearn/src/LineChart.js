import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register the necessary components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const LineChart = ({ data, label }) => {
  const chartData = {
    labels: Array.from({ length: data.length }, (_, i) => i + 1), // x-axis labels, can be customized
    datasets: [
      {
        label: label,
        data: data,
        fill: false,
        backgroundColor: 'rgba(75,192,192,0.2)',
        borderColor: 'rgba(75,192,192,1)',
        tension: 0.1,
      },
    ],
  };

  const options = {
    responsive: true,
    scales: {
      x: {
        type: 'category', // Use 'category' for non-time-based x-axis labels
        display: true,
        title: {
          display: true,
          text: 'Last 20 Data Points',
        },
      },
      y: {
        type: 'linear', // This is the linear scale for the y-axis
        display: true,
        title: {
          display: true,
          text: label,
        },
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default LineChart;
