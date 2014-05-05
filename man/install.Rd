\name{install}
\alias{install}
\title{Install datasets via the EcoData Retriever.}
\usage{
install(dataset, connection, db_file = NULL, conn_file = NULL,
  data_dir = NULL, log_dir = NULL)
}
\arguments{
  \item{dataset}{the name of the dataset that you wish to
  download}

  \item{connection}{what type of database connection should
  be used. The options include: mysql, postgres, sqlite,
  msaccess, or csv'}

  \item{db_file}{the name of the datbase file the dataset
  should be loaded into}

  \item{conn_file}{the path to the .conn file that contains
  the connection configuration options for mysql and
  postgres databases. This defaults to mysql.conn or
  postgres.conn respectively. The connection file is a
  comma seperated file with four fields: user, password,
  host, and port.}

  \item{data_dir}{the location where the dataset should be
  installed. Only relevant for csv connection types.}

  \item{log_dir}{the location where the retriever log
  should be stored if the progress is not printed to the
  console}
}
\description{
Data is stored in either CSV files or one of the following
database management systems: MySQL, PostgreSQL, SQLite, or
Microsoft Access.
}
\examples{
ecoretriever::install('MCDB', 'csv')
}

