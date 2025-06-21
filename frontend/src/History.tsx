import React, { useState, useEffect } from "react";
import {
  CircularProgress,
  Rating,
  Stepper,
  Step,
  StepLabel,
  StepContent,
} from "@mui/material";
import {
  LocationOn,
  AttachMoney,
  Group,
  Star,
  Delete,
  RateReview,
  EmojiEvents,
} from "@mui/icons-material";
import axios from "axios";
import { Button } from "./components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "./components/ui/dialog";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./components/ui/select";
import { Badge } from "./components/ui/badge";
import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "./components/ui/alert";

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
  const [ratingSuccessDialogOpen, setRatingSuccessDialogOpen] =
    useState<boolean>(false);
  const [duplicateRatingDialogOpen, setDuplicateRatingDialogOpen] =
    useState<boolean>(false);

  const stepLabelStyles = {
    "& .MuiStepLabel-label": {
      color: "var(--muted-foreground)",
    },
    "& .MuiStepLabel-label.Mui-active": {
      color: "var(--foreground)",
      fontWeight: "bold",
    },
    "& .MuiStepLabel-label.Mui-completed": {
      color: "var(--foreground)",
    },
  };

  const stepIconStyles = {
    color: "var(--border)",
    "&.Mui-active": {
      color: "var(--primary)",
    },
    "&.Mui-completed": {
      color: "var(--primary)",
    },
    "& .MuiStepIcon-text": {
      fill: "var(--primary-foreground)",
    },
  };

  const ratingStyles = {
    "& .MuiRating-iconEmpty": {
      color: "hsl(var(--muted-foreground))",
    },
  };

  useEffect(() => {
    loadEventHistory();
  }, []);

  const loadEventHistory = async () => {
    try {
      setLoading(true);
      const response = await axios.get("http://localhost:5000/event-history");
      setSavedEvents(response.data);
    } catch (error) {
      console.error("Failed to load event history:", error);
      setError(
        "Failed to load event history. Please check if the backend server is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteEvent = async (eventId: number) => {
    try {
      await axios.delete(`http://localhost:5000/event-history/${eventId}`);
      setSavedEvents((prev) => prev.filter((event) => event.id !== eventId));
      if (selectedEvent?.id === eventId) {
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
    if (
      !ratingEvent ||
      !ratingFormData.member_name ||
      ratingFormData.rating === 0
    ) {
      return;
    }

    try {
      setSubmittingRating(true);

      const ratingData = {
        ...ratingFormData,
        submitted_at: new Date().toISOString(),
      };

      await axios.post(
        `http://localhost:5000/event-history/${ratingEvent.id}/rate`,
        ratingData
      );

      setSavedEvents((prev) =>
        prev.map((event) =>
          event.id === ratingEvent.id
            ? {
                ...event,
                member_ratings: [...(event.member_ratings || []), ratingData],
              }
            : event
        )
      );

      setRatingDialogOpen(false);
      setRatingEvent(null);
      setRatingSuccessDialogOpen(true);
    } catch (error: any) {
      console.error("Failed to submit rating:", error);
      if (error.response?.status === 409) {
        setDuplicateRatingDialogOpen(true);
      } else {
        alert("Failed to submit rating. Please try again.");
      }
    } finally {
      setSubmittingRating(false);
    }
  };

  const handleRatingFormChange = (field: string, value: any) => {
    setRatingFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleCategoryChange = (category: string, value: number) => {
    setRatingFormData((prev) => ({
      ...prev,
      categories: {
        ...prev.categories,
        [category]: value,
      },
    }));
  };

  const getThemeIcon = (theme: string) => {
    switch (theme) {
      case "fun":
      case "fun 🎉":
        return <EmojiEvents className="h-6 w-6" />;
      default:
        return <Group className="h-6 w-6" />;
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-96">
        <CircularProgress />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-destructive/10 border border-destructive/20 text-destructive p-4 rounded-md">
        <h5 className="font-bold">Error</h5>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-foreground">Event History</h1>
        <p className="text-muted-foreground">
          Review your past team bonding events and member feedback.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {savedEvents.map((event) => (
          <Card key={event.id} className="flex flex-col">
            <CardHeader>
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="flex items-center">
                    <div className="p-2 mr-3 bg-primary/10 rounded-full text-primary">
                      {getThemeIcon(event.theme)}
                    </div>
                    {event.theme.replace(/🎉/g, "")}
                  </CardTitle>
                  <CardDescription className="mt-1">
                    {formatDate(event.date)}
                  </CardDescription>
                </div>
                <div className="flex space-x-2">
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={() => handleRateEvent(event)}
                  >
                    <RateReview className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="destructive"
                    size="icon"
                    onClick={() => handleDeleteEvent(event.id)}
                  >
                    <Delete className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="flex-grow space-y-3">
              <div className="flex items-center text-sm text-muted-foreground">
                <LocationOn className="h-4 w-4 mr-2" /> {event.location}
              </div>
              <div className="flex items-center text-sm text-muted-foreground">
                <Group className="h-4 w-4 mr-2" /> {event.participants.length}{" "}
                participants
              </div>
              <div className="flex items-center text-sm text-muted-foreground">
                <AttachMoney className="h-4 w-4 mr-2" />{" "}
                {event.total_cost.toLocaleString()} VND
              </div>
              <div className="flex flex-wrap gap-2">
                {event.activities.map((activity, index) => (
                  <Badge key={index} variant="secondary">
                    {activity}
                  </Badge>
                ))}
              </div>
            </CardContent>
            <CardFooter className="flex flex-col items-start space-y-2">
              <div className="flex items-center w-full">
                <Star className="h-5 w-5 mr-1 text-yellow-500" />
                <span className="font-semibold mr-2">AI Rating:</span>
                <Rating
                  name="ai-rating"
                  value={event.ai_rating || 0}
                  precision={0.5}
                  readOnly
                  size="small"
                />
                <span className="ml-2 text-sm text-muted-foreground">
                  ({event.ai_rating?.toFixed(1) || "N/A"})
                </span>
              </div>
              <div className="flex items-center w-full">
                <Group className="h-5 w-5 mr-1 text-blue-500" />
                <span className="font-semibold mr-2">Member Avg:</span>
                <Rating
                  name="member-avg"
                  value={event.rating || 0}
                  precision={0.5}
                  readOnly
                  size="small"
                />
                <span className="ml-2 text-sm text-muted-foreground">
                  ({event.rating?.toFixed(1) || "N/A"})
                </span>
              </div>
            </CardFooter>
          </Card>
        ))}
      </div>

      <Dialog open={ratingDialogOpen} onOpenChange={setRatingDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Rate Event: {ratingEvent?.theme}</DialogTitle>
            <DialogDescription>
              Your feedback helps improve future events.
            </DialogDescription>
          </DialogHeader>
          <div className="py-4">
            <Stepper
              activeStep={activeStep}
              orientation="vertical"
              sx={{
                "& .MuiStepConnector-line": {
                  borderColor: "var(--border)",
                },
              }}
            >
              <Step>
                <StepLabel
                  StepIconProps={{ sx: stepIconStyles }}
                  sx={stepLabelStyles}
                >
                  <span className="text-foreground">Your Name</span>
                </StepLabel>
                <StepContent>
                  <Label>Select Your Name</Label>
                  <Select
                    value={ratingFormData.member_name}
                    onValueChange={(value) =>
                      handleRatingFormChange("member_name", value)
                    }
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select your name" />
                    </SelectTrigger>
                    <SelectContent>
                      {ratingEvent?.participants.map((p) => (
                        <SelectItem key={p} value={p}>
                          {p}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <div className="mt-4">
                    <Button
                      disabled={!ratingFormData.member_name}
                      onClick={() => setActiveStep(1)}
                    >
                      Next
                    </Button>
                  </div>
                </StepContent>
              </Step>
              <Step>
                <StepLabel
                  StepIconProps={{ sx: stepIconStyles }}
                  sx={stepLabelStyles}
                >
                  <span className="text-foreground">Rate Categories</span>
                </StepLabel>
                <StepContent>
                  <div className="space-y-4">
                    {Object.keys(ratingFormData.categories).map(
                      (category) => (
                        <div key={category}>
                          <Label className="capitalize">{category}</Label>
                          <Rating
                            value={
                              ratingFormData.categories[
                                category as keyof typeof ratingFormData.categories
                              ]
                            }
                            onChange={(event, newValue) => {
                              handleCategoryChange(
                                category as keyof typeof ratingFormData.categories,
                                newValue || 0
                              );
                            }}
                            sx={ratingStyles}
                          />
                        </div>
                      )
                    )}
                  </div>
                  <div className="mt-4 space-x-2">
                    <Button variant="outline" onClick={() => setActiveStep(0)}>
                      Back
                    </Button>
                    <Button onClick={() => setActiveStep(2)}>Next</Button>
                  </div>
                </StepContent>
              </Step>
              <Step>
                <StepLabel
                  StepIconProps={{ sx: stepIconStyles }}
                  sx={stepLabelStyles}
                >
                  <span className="text-foreground">Overall Feedback</span>
                </StepLabel>
                <StepContent>
                  <div className="space-y-2">
                    <Label>Overall Rating</Label>
                    <Rating
                      name="overall"
                      value={ratingFormData.rating}
                      onChange={(event, newValue) => {
                        handleRatingFormChange("rating", newValue || 0);
                      }}
                      size="large"
                      sx={ratingStyles}
                    />
                  </div>
                  <div className="space-y-2 mt-4">
                    <Label>Feedback (Optional)</Label>
                    <Input
                      value={ratingFormData.feedback}
                      onChange={(e) =>
                        handleRatingFormChange("feedback", e.target.value)
                      }
                      placeholder="What did you like or dislike?"
                    />
                  </div>
                  <div className="mt-4 space-x-2">
                    <Button variant="outline" onClick={() => setActiveStep(1)}>
                      Back
                    </Button>
                    <Button
                      onClick={handleRatingSubmit}
                      disabled={submittingRating}
                    >
                      {submittingRating && (
                        <CircularProgress size={20} className="mr-2" />
                      )}
                      Submit Rating
                    </Button>
                  </div>
                </StepContent>
              </Step>
            </Stepper>
          </div>
        </DialogContent>
      </Dialog>

      <Dialog open={ratingSuccessDialogOpen} onOpenChange={setRatingSuccessDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center">
              <div className="w-10 h-10 flex items-center justify-center rounded-full bg-green-500 text-white mr-3">
                <span className="text-xl">✓</span>
              </div>
              <span className="font-bold">Rating Submitted!</span>
            </DialogTitle>
          </DialogHeader>
          <DialogDescription className="py-4 space-y-2">
            <p>Your feedback has been successfully recorded.</p>
            <Alert variant="info">
              <AlertDescription>
                Thank you for helping us improve future team events!
              </AlertDescription>
            </Alert>
          </DialogDescription>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setRatingSuccessDialogOpen(false)}
            >
              Close
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog
        open={duplicateRatingDialogOpen}
        onOpenChange={setDuplicateRatingDialogOpen}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center">
              <div className="w-10 h-10 flex items-center justify-center rounded-full bg-amber-500 text-white mr-3">
                <span className="text-xl">⚠</span>
              </div>
              <span className="font-bold">Already Rated</span>
            </DialogTitle>
          </DialogHeader>
          <DialogDescription className="py-4 space-y-2">
            <p>You have already rated this event.</p>
            <Alert variant="warning">
              <AlertDescription>
                Each team member can only submit one rating per event to ensure
                fair feedback.
              </AlertDescription>
            </Alert>
          </DialogDescription>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setDuplicateRatingDialogOpen(false)}
            >
              Close
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default History; 