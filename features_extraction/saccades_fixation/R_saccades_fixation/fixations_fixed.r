function (fixations) 
{
  stats <- data.frame(mean = double(10), sd = double(10), 
    row.names = c("Number of trials", "Duration of trials", 
      "No. of fixations per trial", "Duration of fixations - Mean", 
      "Duration of fixations - Median", "Dispersion horizontal", 
      "Dispersion vertical", "Peak velocity horizontal", 
      "Peak velocity vertical", "% of Long fixations"))
  stats["Number of trials", ] <- c(length(unique(fixations$trial)), 
    NA)
  s <- tapply(fixations$start, fixations$trial, min)
  e <- tapply(fixations$end, fixations$trial, max)
  tdur <- e - s
  stats["Duration of trials", ] <- c(mean(tdur), stats::sd(tdur))
  n <- tapply(fixations$start, fixations$trial, length)
  stats["No. of fixations per trial", ] <- c(mean(n), stats::sd(n))
  stats["Duration of fixations - Mean", ] <- c(mean(fixations$dur), 
    stats::sd(fixations$dur))
  stats["Duration of fixations - Median", ] <- c(median(fixations$dur), 
    stats::sd(fixations$dur))
  stats["Dispersion horizontal", ] <- c(mean(fixations$mad.x, 
    na.rm = TRUE), stats::sd(fixations$mad.x, na.rm = TRUE))
  stats["Dispersion vertical", ] <- c(mean(fixations$mad.y, 
    na.rm = TRUE), stats::sd(fixations$mad.y, na.rm = TRUE))
  stats["Peak velocity horizontal", ] <- c(mean(fixations$peak.vx, 
    na.rm = T), stats::sd(fixations$peak.vx, na.rm = T))
  stats["Peak velocity vertical", ] <- c(mean(fixations$peak.vy, 
    na.rm = T), stats::sd(fixations$peak.vy, na.rm = T))
  stats["% of Long fixations", ] <- (mean(fixations$dur > 
    150))
  stats
}