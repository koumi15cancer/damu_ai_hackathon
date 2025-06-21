import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  Card,
  CardContent,
  Chip,
  Grid,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  IconButton,
  Alert,
  CircularProgress,
  Divider,
  Rating,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Avatar,
  AvatarGroup,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormLabel,
  Checkbox,
  FormGroup,
} from "@mui/material";
import {
  LocationOn,
  AttachMoney,
  Group,
  Star,
  Schedule,
  Directions,
  ExpandMore,
  Delete,
  RateReview,
  ThumbUp,
  ThumbDown,
  EmojiEvents,
  Restaurant,
  LocalBar,
  SportsEsports,
  Nature,
  Psychology,
  Science,
} from "@mui/icons-material";
import axios from "axios";

interface SavedEvent {
  id: number;
  date: string;
  theme: string;
  location: string;
  participants: string[];
  activities: string[];
  total_cost: number;
  phases?: EventPhase[];
  fit_analysis?: string;
  rating?: number;
  ai_rating?: number;
  member_ratings?: MemberRating[];
  contribution_needed?: number;
}

interface EventPhase {
  activity: string;
  location: string;
  map_link: string;
  cost: number;
  indicators: string[];
}

interface MemberRating {
  member_name: string;
  rating: number;
  feedback: string;
  categories: {
    fun: number;
    organization: number;
    value: number;
    overall: number;
  };
  submitted_at: string;
}

interface RatingFormData {
  member_name: string;
  rating: number;
  feedback: string;
  categories: {
    fun: number;
    organization: number;
    value: number;
    overall: number;
  };
}

const History: React.FC = () => {
  const [savedEvents, setSavedEvents] = useState<SavedEvent[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>("");
  const [selectedEvent, setSelectedEvent] = useState<SavedEvent | null>(null);
  const [dialogOpen, setDialogOpen] = useState<boolean>(false);
  const [ratingDialogOpen, setRatingDialogOpen] = useState<boolean>(false);
  const [ratingEvent, setRatingEvent] = useState<SavedEvent | null>(null);
  const [ratingFormData, setRatingFormData] = useState<RatingFormData>({
    member_name: "",
    rating: 0,
    feedback: "",
    categories: {
      fun: 0,
      organization: 0,
      value: 0,
      overall: 0,
    },
  });
  const [activeStep, setActiveStep] = useState<number>(0);
  const [submittingRating, setSubmittingRating] = useState<boolean>(false);
  const [ratingSuccessDialogOpen, setRatingSuccessDialogOpen] = useState<boolean>(false);
  const [submittedRating, setSubmittedRating] = useState<any>(null);

  useEffect(() => {
    loadEventHistory();
  }, []);

  // Debug effect for success dialog
  useEffect(() => {
    console.log("🎯 ratingSuccessDialogOpen changed:", ratingSuccessDialogOpen);
    console.log("📊 submittedRating:", submittedRating);
    console.log("🎪 ratingEvent:", ratingEvent);
  }, [ratingSuccessDialogOpen, submittedRating, ratingEvent]);

  const loadEventHistory = async () => {
    try {
      setLoading(true);
      const response = await axios.get("http://localhost:5000/event-history");
      setSavedEvents(response.data);
    } catch (error) {
      console.error("Failed to load event history:", error);
      setError("Failed to load event history. Please check if the backend server is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleEventClick = (event: SavedEvent) => {
    setSelectedEvent(event);
    setDialogOpen(true);
  };

  const handleDeleteEvent = async (eventId: number) => {
    try {
      await axios.delete(`http://localhost:5000/event-history/${eventId}`);
      setSavedEvents(prev => prev.filter(event => event.id !== eventId));
      if (selectedEvent?.id === eventId) {
        setDialogOpen(false);
        setSelectedEvent(null);
      }
    } catch (error) {
      console.error("Failed to delete event:", error);
      setError("Failed to delete event. Please try again.");
    }
  };

  const handleRateEvent = (event: SavedEvent) => {
    setRatingEvent(event);
    setRatingFormData({
      member_name: "",
      rating: 0,
      feedback: "",
      categories: {
        fun: 0,
        organization: 0,
        value: 0,
        overall: 0,
      },
    });
    setActiveStep(0);
    setRatingDialogOpen(true);
  };

  const handleRatingSubmit = async () => {
    console.log("🚀 handleRatingSubmit called");
    console.log("ratingEvent:", ratingEvent);
    console.log("ratingFormData:", ratingFormData);
    
    if (!ratingEvent || !ratingFormData.member_name || ratingFormData.rating === 0) {
      console.log("❌ Validation failed");
      console.log("ratingEvent exists:", !!ratingEvent);
      console.log("member_name:", ratingFormData.member_name);
      console.log("rating:", ratingFormData.rating);
      return;
    }

    try {
      console.log("📝 Starting rating submission...");
      setSubmittingRating(true);
      
      const ratingData = {
        ...ratingFormData,
        submitted_at: new Date().toISOString(),
      };

      console.log("📊 Rating data to submit:", ratingData);

      const response = await axios.post(`http://localhost:5000/event-history/${ratingEvent.id}/rate`, ratingData);
      
      console.log("✅ Rating submitted successfully:", response.data);
      
      // Update local state
      setSavedEvents(prev => prev.map(event => 
        event.id === ratingEvent.id 
          ? {
              ...event,
              member_ratings: [...(event.member_ratings || []), ratingData]
            }
          : event
      ));

      console.log("🔄 Closing rating dialog and opening success dialog...");
      setRatingDialogOpen(false);
      setRatingSuccessDialogOpen(true);
      setSubmittedRating(ratingData);
      
      console.log("✅ Success dialog should now be open");
      
    } catch (error: any) {
      console.error("❌ Failed to submit rating:", error);
      if (error.response?.status === 409) {
        alert("You have already rated this event. Each member can only rate once.");
      } else {
        alert("Failed to submit rating. Please try again.");
      }
    } finally {
      setSubmittingRating(false);
    }
  };

  const handleRatingFormChange = (field: string, value: any) => {
    setRatingFormData(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleCategoryChange = (category: string, value: number) => {
    setRatingFormData(prev => ({
      ...prev,
      categories: {
        ...prev.categories,
        [category]: value,
      },
    }));
  };

  const canRateEvent = (event: SavedEvent, memberName: string) => {
    if (!event.member_ratings) return true;
    return !event.member_ratings.some(rating => rating.member_name === memberName);
  };

  const handleSuccessDialogClose = () => {
    setRatingSuccessDialogOpen(false);
    setRatingEvent(null);
    setSubmittedRating(null);
    loadEventHistory(); // Refresh to show updated ratings
  };

  const getThemeIcon = (theme: string) => {
    switch (theme) {
      case "fun 🎉":
      case "fun":
        return "🎉";
      case "chill 🧘":
      case "chill":
        return "🧘";
      case "outdoor 🌤":
      case "outdoor":
        return "🌤";
      default:
        return "🎯";
    }
  };

  const getThemeColor = (theme: string) => {
    switch (theme) {
      case "fun 🎉":
      case "fun":
        return "#ff6b6b";
      case "chill 🧘":
      case "chill":
        return "#4ecdc4";
      case "outdoor 🌤":
      case "outdoor":
        return "#45b7d1";
      default:
        return "#95a5a6";
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '400px' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom sx={{ mb: 3 }}>
        📚 Event History
      </Typography>

      {/* Debug button - remove after testing */}
      <Button
        variant="outlined"
        onClick={() => {
          console.log("🧪 Testing success dialog manually");
          setSubmittedRating({
            member_name: "Test User",
            rating: 5,
            feedback: "Test feedback",
            categories: { fun: 5, organization: 4, value: 4, overall: 5 }
          });
          setRatingSuccessDialogOpen(true);
        }}
        sx={{ mb: 2 }}
      >
        Test Success Dialog
      </Button>

      {savedEvents.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No saved events yet
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Generate and save plans to see them here!
          </Typography>
        </Paper>
      ) : (
        <Grid container spacing={3}>
          {savedEvents.map((event) => (
            <Grid item xs={12} md={6} lg={4} key={event.id}>
              <Card 
                sx={{ 
                  height: '100%', 
                  cursor: 'pointer',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 4
                  }
                }}
                onClick={() => handleEventClick(event)}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Box
                      sx={{
                        backgroundColor: getThemeColor(event.theme),
                        borderRadius: '50%',
                        p: 1,
                        mr: 2,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: 40,
                        height: 40
                      }}
                    >
                      <Typography variant="h6">{getThemeIcon(event.theme)}</Typography>
                    </Box>
                    <Box sx={{ flexGrow: 1 }}>
                      <Typography variant="h6" component="div">
                        {event.theme}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {formatDate(event.date)}
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <IconButton
                        size="small"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleRateEvent(event);
                        }}
                        sx={{ 
                          color: event.member_ratings && event.member_ratings.length > 0 
                            ? 'success.main' 
                            : 'primary.main' 
                        }}
                        title={event.member_ratings && event.member_ratings.length > 0 
                          ? `${event.member_ratings.length} rating(s) submitted` 
                          : 'Rate this event'
                        }
                      >
                        <RateReview />
                      </IconButton>
                      <IconButton
                        size="small"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDeleteEvent(event.id);
                        }}
                        sx={{ color: 'error.main' }}
                      >
                        <Delete />
                      </IconButton>
                    </Box>
                  </Box>

                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <LocationOn color="primary" sx={{ mr: 1, fontSize: 20 }} />
                    <Typography variant="body2" color="text.secondary">
                      {event.location}
                    </Typography>
                  </Box>

                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Group color="primary" sx={{ mr: 1, fontSize: 20 }} />
                    <Typography variant="body2" color="text.secondary">
                      {event.participants.length} participants
                    </Typography>
                  </Box>

                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <AttachMoney color="primary" sx={{ mr: 1, fontSize: 20 }} />
                    <Typography variant="h6" color="primary" sx={{ fontWeight: 'bold' }}>
                      {event.total_cost.toLocaleString()} VND
                    </Typography>
                  </Box>

                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {event.activities.slice(0, 3).map((activity, index) => (
                      <Chip
                        key={index}
                        label={activity}
                        size="small"
                        variant="outlined"
                      />
                    ))}
                    {event.activities.length > 3 && (
                      <Chip
                        label={`+${event.activities.length - 3} more`}
                        size="small"
                        variant="outlined"
                      />
                    )}
                  </Box>

                  {event.ai_rating && (
                    <Box sx={{ display: 'flex', alignItems: 'center', mt: 2 }}>
                      <Rating value={event.ai_rating} readOnly size="small" />
                      <Typography variant="body2" sx={{ ml: 1 }}>
                        AI Rating: {event.ai_rating}/5
                      </Typography>
                    </Box>
                  )}

                  {event.member_ratings && event.member_ratings.length > 0 && (
                    <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                      <Rating value={event.rating} readOnly size="small" />
                      <Typography variant="body2" sx={{ ml: 1 }}>
                        Member Avg: {event.rating}/5
                      </Typography>
                    </Box>
                  )}

                  {event.member_ratings && event.member_ratings.length > 0 && (
                    <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                      <AvatarGroup max={3} sx={{ mr: 1 }}>
                        {event.member_ratings.slice(0, 3).map((rating, index) => (
                          <Avatar key={index} sx={{ width: 24, height: 24, fontSize: '0.75rem' }}>
                            {rating.member_name.charAt(0)}
                          </Avatar>
                        ))}
                      </AvatarGroup>
                      <Typography variant="body2" color="text.secondary">
                        {event.member_ratings.length} member rating(s)
                      </Typography>
                    </Box>
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Event Detail Dialog */}
      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        {selectedEvent && (
          <>
            <DialogTitle>
              <Box sx={{ display: "flex", alignItems: "center" }}>
                <Box
                  sx={{
                    backgroundColor: getThemeColor(selectedEvent.theme),
                    borderRadius: "50%",
                    p: 1,
                    mr: 2,
                  }}
                >
                  <Typography variant="h6">{getThemeIcon(selectedEvent.theme)}</Typography>
                </Box>
                <Box sx={{ flexGrow: 1 }}>
                  <Typography variant="h5" sx={{ fontWeight: "bold" }}>
                    {selectedEvent.theme}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {formatDate(selectedEvent.date)}
                  </Typography>
                </Box>
              </Box>
            </DialogTitle>

            <DialogContent>
              <Grid container spacing={3}>
                <Grid item xs={12} md={8}>
                  {selectedEvent.phases ? (
                    <>
                      <Typography variant="h6" gutterBottom>
                        📍 Event Phases
                      </Typography>
                      {selectedEvent.phases.map((phase, index) => (
                        <Paper key={index} sx={{ p: 2, mb: 2 }}>
                          <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                            <Typography variant="h6" sx={{ flexGrow: 1 }}>
                              Phase {index + 1}: {phase.activity}
                            </Typography>
                            <Chip
                              label={`${phase.cost.toLocaleString()} VND`}
                              color="primary"
                              size="small"
                            />
                          </Box>
                          
                          <List dense>
                            <ListItem>
                              <ListItemIcon>
                                <LocationOn color="primary" />
                              </ListItemIcon>
                              <ListItemText
                                primary="Address"
                                secondary={phase.location}
                              />
                            </ListItem>

                            {phase.map_link && (
                              <ListItem>
                                <ListItemIcon>
                                  <Directions color="primary" />
                                </ListItemIcon>
                                <ListItemText
                                  primary="Google Maps"
                                  secondary={
                                    <a
                                      href={phase.map_link}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                    >
                                      Open in Maps
                                    </a>
                                  }
                                />
                              </ListItem>
                            )}
                          </List>

                          <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
                            {phase.indicators.map((indicator, idx) => (
                              <Chip
                                key={idx}
                                label={indicator}
                                size="small"
                                color={
                                  indicator === "indoor"
                                    ? "primary"
                                    : indicator === "outdoor"
                                    ? "secondary"
                                    : indicator === "vegetarian-friendly"
                                    ? "success"
                                    : indicator === "alcohol-friendly"
                                    ? "warning"
                                    : "default"
                                }
                              />
                            ))}
                          </Box>
                        </Paper>
                      ))}
                    </>
                  ) : (
                    <>
                      <Typography variant="h6" gutterBottom>
                        🎯 Activities
                      </Typography>
                      <List>
                        {selectedEvent.activities.map((activity, index) => (
                          <ListItem key={index}>
                            <ListItemIcon>
                              <Star color="primary" />
                            </ListItemIcon>
                            <ListItemText primary={activity} />
                          </ListItem>
                        ))}
                      </List>
                    </>
                  )}
                </Grid>

                <Grid item xs={12} md={4}>
                  <Paper sx={{ p: 2, mb: 2 }}>
                    <Typography variant="h6" gutterBottom>
                      💰 Cost Breakdown
                    </Typography>
                    <Typography
                      variant="h4"
                      sx={{ color: "#27ae60", fontWeight: "bold" }}
                    >
                      {selectedEvent.total_cost.toLocaleString()} VND
                    </Typography>
                    <Typography variant="body2" sx={{ color: "#7f8c8d" }}>
                      total cost
                    </Typography>
                    {selectedEvent.contribution_needed && selectedEvent.contribution_needed > 0 && (
                      <Alert severity="warning" sx={{ mt: 1 }}>
                        Additional contribution:{" "}
                        {selectedEvent.contribution_needed.toLocaleString()} VND
                      </Alert>
                    )}
                  </Paper>

                  <Paper sx={{ p: 2, mb: 2 }}>
                    <Typography variant="h6" gutterBottom>
                      👥 Participants
                    </Typography>
                    <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
                      {selectedEvent.participants.map((participant, index) => (
                        <Chip
                          key={index}
                          label={participant}
                          size="small"
                          color="primary"
                          variant="outlined"
                        />
                      ))}
                    </Box>
                  </Paper>

                  {selectedEvent.fit_analysis && (
                    <Paper sx={{ p: 2, mb: 2 }}>
                      <Typography variant="h6" gutterBottom>
                        👥 Team Fit
                      </Typography>
                      <Typography variant="body2" sx={{ color: "#7f8c8d" }}>
                        {selectedEvent.fit_analysis}
                      </Typography>
                    </Paper>
                  )}

                  {selectedEvent.ai_rating && (
                    <Paper sx={{ p: 2, mb: 2 }}>
                      <Typography variant="h6" gutterBottom>
                        🤖 AI Rating
                      </Typography>
                      <Box sx={{ display: "flex", alignItems: "center" }}>
                        <Rating value={selectedEvent.ai_rating} readOnly size="small" />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                          {selectedEvent.ai_rating}/5
                        </Typography>
                      </Box>
                      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        AI-generated rating based on event planning criteria
                      </Typography>
                    </Paper>
                  )}

                  {selectedEvent.member_ratings && selectedEvent.member_ratings.length > 0 && (
                    <Paper sx={{ p: 2, mb: 2 }}>
                      <Typography variant="h6" gutterBottom>
                        👥 Member Average Rating
                      </Typography>
                      <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                        <Rating value={selectedEvent.rating} readOnly size="small" />
                        <Typography variant="body2" sx={{ ml: 1 }}>
                          {selectedEvent.rating}/5 ({selectedEvent.member_ratings.length} ratings)
                        </Typography>
                      </Box>
                      <Typography variant="body2" color="text.secondary">
                        Average rating from team member feedback
                      </Typography>
                    </Paper>
                  )}

                  {selectedEvent.member_ratings && selectedEvent.member_ratings.length > 0 && (
                    <Paper sx={{ p: 2 }}>
                      <Typography variant="h6" gutterBottom>
                        👥 Individual Member Ratings ({selectedEvent.member_ratings.length})
                      </Typography>
                      <Box sx={{ maxHeight: 200, overflowY: 'auto' }}>
                        {selectedEvent.member_ratings.map((rating, index) => (
                          <Box key={index} sx={{ mb: 2, p: 1, border: '1px solid #e0e0e0', borderRadius: 1 }}>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                              <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                                {rating.member_name}
                              </Typography>
                              <Rating value={rating.rating} readOnly size="small" />
                            </Box>
                            {rating.feedback && (
                              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                                "{rating.feedback}"
                              </Typography>
                            )}
                            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                              {Object.entries(rating.categories).map(([category, value]) => (
                                <Chip
                                  key={category}
                                  label={`${category}: ${value}/5`}
                                  size="small"
                                  variant="outlined"
                                />
                              ))}
                            </Box>
                            <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                              {new Date(rating.submitted_at).toLocaleDateString()}
                            </Typography>
                          </Box>
                        ))}
                      </Box>
                    </Paper>
                  )}
                </Grid>
              </Grid>
            </DialogContent>

            <DialogActions>
              <Button onClick={() => setDialogOpen(false)}>Close</Button>
              <Button
                variant="outlined"
                color="primary"
                onClick={() => {
                  setDialogOpen(false);
                  handleRateEvent(selectedEvent);
                }}
                startIcon={<RateReview />}
              >
                Rate Event
              </Button>
              <Button
                variant="contained"
                color="error"
                onClick={() => {
                  handleDeleteEvent(selectedEvent.id);
                  setDialogOpen(false);
                }}
              >
                Delete Event
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>

      {/* Rating Modal */}
      <Dialog
        open={ratingDialogOpen}
        onClose={() => setRatingDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        {ratingEvent && (
          <>
            <DialogTitle>
              <Box sx={{ display: "flex", alignItems: "center" }}>
                <Box
                  sx={{
                    backgroundColor: getThemeColor(ratingEvent.theme),
                    borderRadius: "50%",
                    p: 1,
                    mr: 2,
                  }}
                >
                  <Typography variant="h6">{getThemeIcon(ratingEvent.theme)}</Typography>
                </Box>
                <Box sx={{ flexGrow: 1 }}>
                  <Typography variant="h5" sx={{ fontWeight: "bold" }}>
                    Rate This Event
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {ratingEvent.theme} • {formatDate(ratingEvent.date)}
                  </Typography>
                </Box>
              </Box>
            </DialogTitle>

            <DialogContent>
              <Stepper activeStep={activeStep} orientation="vertical" sx={{ mb: 3 }}>
                <Step>
                  <StepLabel>Select Your Name</StepLabel>
                  <StepContent>
                    <FormControl fullWidth sx={{ mt: 2 }}>
                      <InputLabel>Your Name</InputLabel>
                      <Select
                        value={ratingFormData.member_name}
                        label="Your Name"
                        onChange={(e) => handleRatingFormChange('member_name', e.target.value)}
                      >
                        {ratingEvent.participants.map((participant) => (
                          <MenuItem key={participant} value={participant}>
                            {participant}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                    <Box sx={{ mt: 2 }}>
                      <Button
                        variant="contained"
                        onClick={() => setActiveStep(1)}
                        disabled={!ratingFormData.member_name}
                      >
                        Continue
                      </Button>
                    </Box>
                  </StepContent>
                </Step>

                <Step>
                  <StepLabel>Overall Rating</StepLabel>
                  <StepContent>
                    <Box sx={{ mt: 2, textAlign: 'center' }}>
                      <Typography variant="h6" gutterBottom>
                        How would you rate this event overall?
                      </Typography>
                      <Rating
                        value={ratingFormData.rating}
                        onChange={(_, value) => handleRatingFormChange('rating', value || 0)}
                        size="large"
                        sx={{ fontSize: '2rem', mb: 2 }}
                      />
                      <Typography variant="body2" color="text.secondary">
                        {ratingFormData.rating === 0 && "Select a rating"}
                        {ratingFormData.rating === 1 && "Poor"}
                        {ratingFormData.rating === 2 && "Fair"}
                        {ratingFormData.rating === 3 && "Good"}
                        {ratingFormData.rating === 4 && "Very Good"}
                        {ratingFormData.rating === 5 && "Excellent"}
                      </Typography>
                    </Box>
                    <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                      <Button onClick={() => setActiveStep(0)}>Back</Button>
                      <Button
                        variant="contained"
                        onClick={() => setActiveStep(2)}
                        disabled={ratingFormData.rating === 0}
                      >
                        Continue
                      </Button>
                    </Box>
                  </StepContent>
                </Step>

                <Step>
                  <StepLabel>Detailed Categories</StepLabel>
                  <StepContent>
                    <Box sx={{ mt: 2 }}>
                      <Typography variant="h6" gutterBottom>
                        Rate specific aspects of the event
                      </Typography>
                      
                      <Grid container spacing={3}>
                        <Grid item xs={12} md={6}>
                          <Box sx={{ mb: 3 }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                              <EmojiEvents color="primary" sx={{ mr: 1 }} />
                              <Typography variant="subtitle1">Fun Factor</Typography>
                            </Box>
                            <Rating
                              value={ratingFormData.categories.fun}
                              onChange={(_, value) => handleCategoryChange('fun', value || 0)}
                              size="small"
                            />
                          </Box>
                        </Grid>

                        <Grid item xs={12} md={6}>
                          <Box sx={{ mb: 3 }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                              <Schedule color="primary" sx={{ mr: 1 }} />
                              <Typography variant="subtitle1">Organization</Typography>
                            </Box>
                            <Rating
                              value={ratingFormData.categories.organization}
                              onChange={(_, value) => handleCategoryChange('organization', value || 0)}
                              size="small"
                            />
                          </Box>
                        </Grid>

                        <Grid item xs={12} md={6}>
                          <Box sx={{ mb: 3 }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                              <AttachMoney color="primary" sx={{ mr: 1 }} />
                              <Typography variant="subtitle1">Value for Money</Typography>
                            </Box>
                            <Rating
                              value={ratingFormData.categories.value}
                              onChange={(_, value) => handleCategoryChange('value', value || 0)}
                              size="small"
                            />
                          </Box>
                        </Grid>

                        <Grid item xs={12} md={6}>
                          <Box sx={{ mb: 3 }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                              <Star color="primary" sx={{ mr: 1 }} />
                              <Typography variant="subtitle1">Overall Experience</Typography>
                            </Box>
                            <Rating
                              value={ratingFormData.categories.overall}
                              onChange={(_, value) => handleCategoryChange('overall', value || 0)}
                              size="small"
                            />
                          </Box>
                        </Grid>
                      </Grid>
                    </Box>
                    <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                      <Button onClick={() => setActiveStep(1)}>Back</Button>
                      <Button
                        variant="contained"
                        onClick={() => setActiveStep(3)}
                      >
                        Continue
                      </Button>
                    </Box>
                  </StepContent>
                </Step>

                <Step>
                  <StepLabel>Additional Feedback</StepLabel>
                  <StepContent>
                    <Box sx={{ mt: 2 }}>
                      <Typography variant="h6" gutterBottom>
                        Share your thoughts (optional)
                      </Typography>
                      <TextField
                        fullWidth
                        multiline
                        rows={4}
                        placeholder="What did you enjoy most? What could be improved? Any suggestions for future events?"
                        value={ratingFormData.feedback}
                        onChange={(e) => handleRatingFormChange('feedback', e.target.value)}
                        sx={{ mb: 2 }}
                      />
                      
                      <Alert severity="info" sx={{ mb: 2 }}>
                        <Typography variant="body2">
                          Your feedback helps us improve future team bonding events. Thank you for taking the time to share your experience!
                        </Typography>
                      </Alert>
                    </Box>
                    <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                      <Button onClick={() => setActiveStep(2)}>Back</Button>
                      <Button
                        variant="contained"
                        onClick={handleRatingSubmit}
                        disabled={submittingRating}
                        startIcon={submittingRating ? <CircularProgress size={20} /> : null}
                      >
                        {submittingRating ? 'Submitting...' : 'Submit Rating'}
                      </Button>
                    </Box>
                  </StepContent>
                </Step>
              </Stepper>
            </DialogContent>
          </>
        )}
      </Dialog>

      {/* Rating Success Dialog */}
      <Dialog
        open={ratingSuccessDialogOpen}
        onClose={handleSuccessDialogClose}
        maxWidth="sm"
        fullWidth
      >
        {submittedRating && (
          <>
            <DialogTitle>
              <Box sx={{ display: "flex", alignItems: "center" }}>
                <Box
                  sx={{
                    backgroundColor: "#4caf50",
                    borderRadius: "50%",
                    p: 1,
                    mr: 2,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    width: 40,
                    height: 40
                  }}
                >
                  <Typography variant="h6" sx={{ color: "white" }}>✓</Typography>
                </Box>
                <Typography variant="h6" sx={{ fontWeight: "bold" }}>
                  Rating Submitted Successfully!
                </Typography>
              </Box>
            </DialogTitle>

            <DialogContent>
              <Box sx={{ textAlign: 'center', mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Thank you for your feedback, {submittedRating.member_name}!
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Your rating helps us improve future team bonding events.
                </Typography>
                
                <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
                  <Rating 
                    value={submittedRating.rating} 
                    readOnly 
                    size="large"
                    sx={{ fontSize: '2rem' }}
                  />
                </Box>
                <Typography variant="h6" color="primary" sx={{ fontWeight: 'bold' }}>
                  {submittedRating.rating}/5 Stars
                </Typography>
              </Box>

              {submittedRating.feedback && (
                <Paper sx={{ p: 2, mb: 2, backgroundColor: '#f5f5f5' }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Your Feedback:
                  </Typography>
                  <Typography variant="body2" sx={{ fontStyle: 'italic' }}>
                    "{submittedRating.feedback}"
                  </Typography>
                </Paper>
              )}

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Category Ratings:
                </Typography>
                <Grid container spacing={1}>
                  {Object.entries(submittedRating.categories).map(([category, value]) => (
                    <Grid item xs={6} key={category}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Typography variant="body2" sx={{ textTransform: 'capitalize' }}>
                          {category}:
                        </Typography>
                        <Rating value={value as number} readOnly size="small" />
                      </Box>
                    </Grid>
                  ))}
                </Grid>
              </Box>

              <Alert severity="success" sx={{ mb: 2 }}>
                <Typography variant="body2">
                  Your rating has been saved and will help improve future events. You can view all ratings in the event details.
                </Typography>
              </Alert>
            </DialogContent>

            <DialogActions>
              <Button onClick={handleSuccessDialogClose}>Close</Button>
              <Button
                variant="contained"
                color="primary"
                onClick={() => {
                  handleSuccessDialogClose();
                  // Refresh the event list to show updated ratings
                  loadEventHistory();
                }}
              >
                View Updated Events
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Box>
  );
};

export default History; 