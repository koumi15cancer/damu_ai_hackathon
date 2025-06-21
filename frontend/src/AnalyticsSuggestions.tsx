import React, { useState, useEffect, useCallback } from "react";
import {
  CircularProgress,
  Alert,
  Divider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
  LinearProgress,
  IconButton,
  Tooltip,
  Snackbar,
  Card,
  CardContent,
  Grid,
  Chip,
  Typography,
  Box,
  Button,
  Container,
  Paper,
} from "@mui/material";
import {
  TrendingUp,
  Lightbulb,
  Psychology,
  Refresh,
  Analytics,
  AttachMoney,
  Group,
  Schedule,
  Update,
  CheckCircle,
} from "@mui/icons-material";
import axios from "axios";

interface Suggestion {
  type: string;
  title: string;
  description: string;
  confidence: number;
  data_points: number;
  category: string;
}

interface AnalyticsSummary {
  total_events: number;
  most_popular_theme: string;
  average_cost: number;
  common_activities: string[];
  rating_trends: string;
  theme_distribution: Record<string, number>;
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
  const [limit, setLimit] = useState<number>(10);
  const [themeFilter, setThemeFilter] = useState<string>("");
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);
  const [isTabVisible, setIsTabVisible] = useState(true);

  // Handle visibility change
  useEffect(() => {
    const handleVisibilityChange = () => {
      setIsTabVisible(!document.hidden);
    };
    document.addEventListener("visibilitychange", handleVisibilityChange);
    return () =>
      document.removeEventListener("visibilitychange", handleVisibilityChange);
  }, []);

  // Load analytics data
  const loadAnalytics = async (forceRefresh = false) => {
    if (loading) return;
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      params.append("limit", limit.toString());
      if (themeFilter) params.append("theme", themeFilter);
      if (forceRefresh) params.append("force_refresh", "true");

      const response = await axios.get(
        `http://localhost:5000/analytics/suggestions?${params}`
      );
      setAnalyticsData(response.data);
      setLastUpdate(new Date());
      if (forceRefresh) setShowSuccessMessage(true);
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to load analytics");
    } finally {
      setLoading(false);
    }
  };

  // Initial load and reload on filter change
  useEffect(() => {
    loadAnalytics();
  }, [limit, themeFilter]);

  // Periodic refresh when tab is visible
  useEffect(() => {
    const interval = setInterval(() => {
      if (isTabVisible) loadAnalytics();
    }, 30 * 60 * 1000); // 30 minutes
    return () => clearInterval(interval);
  }, [isTabVisible]);

  // Listen for custom refresh event (from tab switch)
  useEffect(() => {
    const handleRefreshEvent = () => loadAnalytics(true);
    window.addEventListener("refreshAnalytics", handleRefreshEvent);
    return () =>
      window.removeEventListener("refreshAnalytics", handleRefreshEvent);
  }, []);

  const handleManualRefresh = () => loadAnalytics(true);

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case "theme":
        return <Group />;
      case "activity":
        return <TrendingUp />;
      case "cost":
        return <AttachMoney />;
      case "timing":
        return <Schedule />;
      default:
        return <Lightbulb />;
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case "theme":
        return "primary";
      case "activity":
        return "success";
      case "cost":
        return "warning";
      case "timing":
        return "info";
      default:
        return "default";
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return "success";
    if (confidence >= 0.6) return "warning";
    return "error";
  };

  const formatConfidence = (confidence: number) => {
    return `${(confidence * 100).toFixed(0)}%`;
  };

  if (loading && !analyticsData) {
    return (
      <Container maxWidth='lg' sx={{ py: 4 }}>
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            minHeight: 400,
          }}>
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth='lg' sx={{ py: 4 }} data-analytics-trigger>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 3,
        }}>
        <Box>
          <Typography variant='h4' component='h1' gutterBottom>
            📊 Event Analytics & Suggestions
          </Typography>
          <Typography variant='body1' color='text.secondary'>
            AI-powered insights based on your recent team bonding events
          </Typography>
          {lastUpdate && (
            <Typography
              variant='caption'
              color='text.secondary'
              sx={{ display: "block", mt: 1 }}>
              Last updated: {lastUpdate.toLocaleTimeString()}
            </Typography>
          )}
        </Box>
        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
          {loading && <CircularProgress size={20} />}
          <Tooltip title='Refresh Analytics'>
            <IconButton onClick={handleManualRefresh} disabled={loading}>
              <Refresh />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {/* Filters */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant='h6' gutterBottom>
          <Analytics sx={{ mr: 1, verticalAlign: "middle" }} />
          Analysis Filters
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Events to Analyze</InputLabel>
              <Select
                value={limit.toString()}
                label='Events to Analyze'
                onChange={(e: SelectChangeEvent) =>
                  setLimit(Number(e.target.value))
                }>
                <MenuItem value={5}>Last 5 events</MenuItem>
                <MenuItem value={10}>Last 10 events</MenuItem>
                <MenuItem value={20}>Last 20 events</MenuItem>
                <MenuItem value={50}>Last 50 events</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Filter by Theme</InputLabel>
              <Select
                value={themeFilter}
                label='Filter by Theme'
                onChange={(e: SelectChangeEvent) =>
                  setThemeFilter(e.target.value)
                }>
                <MenuItem value=''>All themes</MenuItem>
                <MenuItem value='fun 🎉'>Fun 🎉</MenuItem>
                <MenuItem value='chill 🧘'>Chill 🧘</MenuItem>
                <MenuItem value='outdoor 🌤'>Outdoor 🌤</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Paper>

      {error && (
        <Alert severity='error' sx={{ mb: 3 }}>
          {error}
          <Button size='small' onClick={handleManualRefresh} sx={{ ml: 2 }}>
            Retry
          </Button>
        </Alert>
      )}

      {loading && analyticsData && (
        <Box sx={{ mb: 3 }}>
          <LinearProgress />
          <Typography variant='body2' color='text.secondary' sx={{ mt: 1 }}>
            Updating analytics...
          </Typography>
        </Box>
      )}

      {analyticsData && (
        <>
          {/* Analytics Summary */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant='h6' gutterBottom>
              📈 Analytics Summary
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} md={3}>
                <Box sx={{ textAlign: "center" }}>
                  <Typography variant='h4' color='primary'>
                    {analyticsData.analytics_summary.total_events}
                  </Typography>
                  <Typography variant='body2' color='text.secondary'>
                    Events Analyzed
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} md={3}>
                <Box sx={{ textAlign: "center" }}>
                  <Typography variant='h4' color='success.main'>
                    {analyticsData.analytics_summary.most_popular_theme}
                  </Typography>
                  <Typography variant='body2' color='text.secondary'>
                    Popular Theme
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} md={3}>
                <Box sx={{ textAlign: "center" }}>
                  <Typography variant='h4' color='warning.main'>
                    {analyticsData.analytics_summary.average_cost.toLocaleString()}{" "}
                    VND
                  </Typography>
                  <Typography variant='body2' color='text.secondary'>
                    Average Cost
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} md={3}>
                <Box sx={{ textAlign: "center" }}>
                  <Typography variant='h4' color='info.main'>
                    {analyticsData.suggestions.length}
                  </Typography>
                  <Typography variant='body2' color='text.secondary'>
                    AI Suggestions
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </Paper>

          {/* AI Suggestions */}
          <Typography variant='h5' gutterBottom>
            💡 AI-Powered Suggestions
          </Typography>

          {analyticsData.suggestions.length === 0 ? (
            <Paper sx={{ p: 3, textAlign: "center" }}>
              <Typography variant='body1' color='text.secondary'>
                No suggestions available. Try analyzing more events or different
                themes.
              </Typography>
            </Paper>
          ) : (
            <Grid container spacing={3}>
              {analyticsData.suggestions.map((suggestion, index) => (
                <Grid item xs={12} md={6} key={index}>
                  <Card
                    sx={{
                      height: "100%",
                      display: "flex",
                      flexDirection: "column",
                    }}>
                    <CardContent sx={{ flexGrow: 1 }}>
                      <Box
                        sx={{
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "flex-start",
                          mb: 2,
                        }}>
                        <Box sx={{ display: "flex", alignItems: "center" }}>
                          {getCategoryIcon(suggestion.category)}
                          <Typography variant='h6' sx={{ ml: 1 }}>
                            {suggestion.title}
                          </Typography>
                        </Box>
                        <Chip
                          label={suggestion.category}
                          size='small'
                          color={getCategoryColor(suggestion.category) as any}
                          variant='outlined'
                        />
                      </Box>
                      <Typography
                        variant='body2'
                        color='text.secondary'
                        sx={{ mb: 2 }}>
                        {suggestion.description}
                      </Typography>
                      <Box
                        sx={{
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "center",
                        }}>
                        <Box sx={{ display: "flex", alignItems: "center" }}>
                          <Typography variant='caption' color='text.secondary'>
                            Confidence:{" "}
                            {formatConfidence(suggestion.confidence)}
                          </Typography>
                          <Box sx={{ ml: 1, width: 60 }}>
                            <LinearProgress
                              variant='determinate'
                              value={suggestion.confidence * 100}
                              color={
                                getConfidenceColor(suggestion.confidence) as any
                              }
                              sx={{ height: 4, borderRadius: 2 }}
                            />
                          </Box>
                        </Box>
                        <Typography variant='caption' color='text.secondary'>
                          Based on {suggestion.data_points} data points
                        </Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          )}
        </>
      )}

      {/* Success Message */}
      <Snackbar
        open={showSuccessMessage}
        autoHideDuration={3000}
        onClose={() => setShowSuccessMessage(false)}
        anchorOrigin={{ vertical: "bottom", horizontal: "right" }}>
        <Alert
          onClose={() => setShowSuccessMessage(false)}
          severity='success'
          icon={<CheckCircle />}>
          Analytics updated successfully!
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default AnalyticsSuggestions;
