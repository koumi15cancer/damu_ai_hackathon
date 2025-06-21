import React, { useState, useEffect, useCallback } from 'react';
import {
  CircularProgress,
  Paper,
  Box,
  Typography,
  Container,
} from '@mui/material';
import {
  TrendingUp,
  Lightbulb,
  Psychology,
  Refresh,
  Analytics,
  Star,
  AttachMoney,
  Group,
  Schedule,
} from '@mui/icons-material';
import axios from 'axios';
import { Button } from './components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from './components/ui/select';
import { Label } from './components/ui/label';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Bot } from 'lucide-react';

interface Suggestion {
  type: string;
  title: string;
  description: string;
  confidence: number;
  data_points: number;
  category: string;
}

interface TimePoint {
  date: string;
  rating?: number;
  theme?: string;
}

interface AnalyticsSummary {
  total_events: number;
  most_popular_theme: string;
  average_cost: number;
  common_activities: string[];
  rating_trends: string;
  theme_distribution: Record<string, number>;
  time_series_data: TimePoint[];
}

interface AnalyticsData {
  suggestions: Suggestion[];
  analytics_summary: AnalyticsSummary;
}

const AnalyticsSuggestions: React.FC = () => {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(
    null
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [limit, setLimit] = useState<string>('10');
  const [themeFilter, setThemeFilter] = useState<string>('');

  const loadAnalytics = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams();
      params.append('limit', limit);
      if (themeFilter) {
        params.append('theme', themeFilter);
      }

      const response = await axios.get(
        `http://localhost:5000/analytics/suggestions?${params}`
      );
      setAnalyticsData(response.data);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load analytics');
    } finally {
      setLoading(false);
    }
  }, [limit, themeFilter]);

  useEffect(() => {
    loadAnalytics();
  }, [loadAnalytics]);

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'theme':
        return <Group className="h-5 w-5" />;
      case 'activity':
        return <TrendingUp className="h-5 w-5" />;
      case 'cost':
        return <AttachMoney className="h-5 w-5" />;
      case 'timing':
        return <Schedule className="h-5 w-5" />;
      default:
        return <Lightbulb className="h-5 w-5" />;
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'text-green-500';
    if (confidence >= 0.6) return 'text-yellow-500';
    return 'text-red-500';
  };

  const formatConfidence = (confidence: number) => {
    return `${(confidence * 100).toFixed(0)}%`;
  };

  // Default data for the chart when real data is insufficient
  const defaultChartData: TimePoint[] = [
    { date: 'Start', rating: 3.0, theme: 'Your first event!' },
    { date: 'Next', rating: 3.5, theme: 'Team building' },
    { date: 'Future', rating: 4.2, theme: 'Company offsite' },
    { date: 'Goal', rating: 4.8, theme: 'Team success!' },
  ];
  
  const CustomTooltip = ({ active, payload, label, hasEnoughData }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="p-2 text-sm bg-background border rounded-lg shadow-sm">
          <p className="font-bold">{hasEnoughData ? new Date(label).toLocaleDateString('en-US', { dateStyle: 'medium' }) : label}</p>
          <p className="text-primary">{`Rating: ${payload[0].value.toFixed(1)} / 5`}</p>
          <p className="text-muted-foreground">{`Theme: ${payload[0].payload.theme}`}</p>
        </div>
      );
    }
    return null;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Bot className="w-12 h-12 animate-spin text-primary" />
      </div>
    );
  }

  if (!analyticsData) {
    return (
      <div className="flex items-center justify-center h-96">
        <Bot className="w-12 h-12 animate-spin text-primary" />
      </div>
    );
  }

  const hasEnoughData = analyticsData.analytics_summary?.time_series_data?.length > 1;
  const chartData = hasEnoughData ? analyticsData.analytics_summary.time_series_data : defaultChartData;

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-foreground">
              📊 Event Analytics & Suggestions
            </h1>
            <p className="text-muted-foreground">
              AI-powered insights based on your recent team bonding events
            </p>
          </div>
          <Button variant="outline" onClick={loadAnalytics} disabled={loading}>
            <Refresh className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Analytics className="mr-2" /> Analysis Filters
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label>Events to Analyze</Label>
                <Select
                  value={limit}
                  onValueChange={(value) => setLimit(value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select number of events" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="5">Last 5 events</SelectItem>
                    <SelectItem value="10">Last 10 events</SelectItem>
                    <SelectItem value="20">Last 20 events</SelectItem>
                    <SelectItem value="50">Last 50 events</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Filter by Theme</Label>
                <Select
                  value={themeFilter}
                  onValueChange={(value) => setThemeFilter(value === "all" ? "" : value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Filter by theme" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All themes</SelectItem>
                    <SelectItem value="fun 🎉">Fun 🎉</SelectItem>
                    <SelectItem value="chill 🧘">Chill 🧘</SelectItem>
                    <SelectItem value="outdoor 🌤">Outdoor 🌤</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {error && (
          <div className="bg-destructive/10 border border-destructive/20 text-destructive p-4 rounded-md">
            <h5 className="font-bold">Error</h5>
            <p>{error}</p>
          </div>
        )}

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="w-5 h-5 mr-2" />
              Event Rating Trend
            </CardTitle>
            {!hasEnoughData && (
              <p className="text-sm text-muted-foreground pt-1">
                This is an example chart. Rate at least two events to see your actual trend.
              </p>
            )}
          </CardHeader>
          <CardContent>
            <div className="w-full h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis 
                    dataKey="date" 
                    stroke="hsl(var(--muted-foreground))" 
                    fontSize={12} 
                    tickLine={false} 
                    axisLine={false} 
                    tickFormatter={(value) => hasEnoughData ? new Date(value).toLocaleDateString('en-US', { month: 'short' }) : value} 
                  />
                  <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} domain={[1, 5]} />
                  <Tooltip content={<CustomTooltip hasEnoughData={hasEnoughData} />} cursor={{ fill: 'hsl(var(--muted))' }} />
                  <Line type="monotone" dataKey="rating" stroke="hsl(var(--primary))" strokeWidth={2} dot={{ r: !hasEnoughData ? 4 : 0 }} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>📈 Analytics Summary</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
              <div>
                <p className="text-3xl font-bold text-primary">
                  {analyticsData.analytics_summary.total_events}
                </p>
                <p className="text-sm text-muted-foreground">
                  Events Analyzed
                </p>
              </div>
              <div>
                <p className="text-xl font-semibold text-green-600">
                  {analyticsData.analytics_summary.most_popular_theme}
                </p>
                <p className="text-sm text-muted-foreground">
                  Most Popular Theme
                </p>
              </div>
              <div>
                <p className="text-xl font-semibold text-amber-600">
                  {analyticsData.analytics_summary.average_cost.toLocaleString()}{' '}
                  VND
                </p>
                <p className="text-sm text-muted-foreground">Average Cost</p>
              </div>
              <div>
                <p className="text-xl font-semibold text-blue-600">
                  {analyticsData.analytics_summary.common_activities.length}
                </p>
                <p className="text-sm text-muted-foreground">
                  Common Activities
                </p>
              </div>
            </div>
            <div className="mt-6">
              <h4 className="font-semibold mb-2">Rating Trend</h4>
              <p className="text-sm text-muted-foreground">
                {analyticsData.analytics_summary.rating_trends}
              </p>
            </div>
            <div className="mt-6">
              <h4 className="font-semibold mb-2">Popular Activities</h4>
              <div className="flex flex-wrap gap-2">
                {analyticsData.analytics_summary.common_activities.map(
                  (activity, index) => (
                    <div
                      key={index}
                      className="bg-secondary text-secondary-foreground px-2 py-1 text-xs rounded"
                    >
                      {activity}
                    </div>
                  )
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Psychology className="mr-2" /> AI-Powered Suggestions
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {analyticsData.suggestions.map((suggestion, index) => (
              <Card key={index} className="bg-muted/30">
                <CardHeader>
                  <CardTitle className="text-base flex items-center">
                    <div className="p-2 mr-3 bg-primary/10 rounded-full text-primary">
                      {getCategoryIcon(suggestion.category)}
                    </div>
                    {suggestion.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground mb-3">
                    {suggestion.description}
                  </p>
                  <div className="flex justify-between items-center text-xs text-muted-foreground">
                    <span>
                      Based on {suggestion.data_points} data point(s)
                    </span>
                    <div className="flex items-center space-x-2">
                      <span>Confidence:</span>
                      <div className="w-24 bg-background rounded-full h-2.5">
                        <div
                          className="bg-primary h-2.5 rounded-full"
                          style={{
                            width: `${suggestion.confidence * 100}%`,
                          }}
                        ></div>
                      </div>
                      <span className={getConfidenceColor(suggestion.confidence)}>
                        {formatConfidence(suggestion.confidence)}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </CardContent>
        </Card>
      </div>
    </Container>
  );
};

export default AnalyticsSuggestions; 