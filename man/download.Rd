\name{download}
\alias{download}
\title{Download datasets via the EcoData Retriever.}
\usage{
download(dataset, path = ".", log_dir = NULL)
}
\arguments{
  \item{dataset}{the name of the dataset that you wish to
  download}

  \item{path}{the path where the data should be downloaded
  to}

  \item{log_dir}{the location where the retriever log
  should be stored if the progress is not printed to the
  console}
}
\description{
Directly downloads data files with no processing, allowing
downloading of non-tabular data.
}
\examples{
\donttest{
ecoretriever::download('MCDB')
## list files downloaded
dir('.', pattern='MCDB')
}
}

