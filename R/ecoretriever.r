#' Install datasets via the EcoData Retriever.
#'
#' Data is stored in either CSV files or one of the following database management
#' systems: MySQL, PostgreSQL, SQLite, or Microsoft Access.
#'
#' @param dataset the name of the dataset that you wish to download
#' @param connection what type of database connection should be used. 
#' The options include: mysql, postgres, sqlite, msaccess, or csv'
#' @param db_file the name of the datbase file the dataset should be loaded 
#' into
#' @param log_dir the location where the retriever log should be stored if
#' the progress is not printed to the console
#' @param user the user argument for connecting data to a database server
#' @param pwd the password argument for connecting data to a database server
#' @param host the host argument for connecting data to a database server
#' @param port the port argument for connecting data to a database server
#' @export
#' @examples
#' install_data('MCDB', 'csv')
install_data = function(dataset, connection, db_file=NULL,
                                log_dir=NULL, user=NULL, pwd=NULL, host=NULL,
                                port=NULL){
  if (missing(connection)) {
    stop("The argument 'connection' must be set to one of the following options: 'mysql', 'postgres', 'sqlite', 'msaccess', or 'csv'")
  }
  else if (connection == 'mysql' | connection == 'postgres') {
    cmd = paste('retriever install', connection, dataset, '--user', user,
                '--password', pwd, '--host', host, '--port', port)
  }
  else if (connection == 'sqlite' | connection == 'msaccess') {
    if (is.null(db_file))
      cmd = paste('retriever install', connection, dataset)
    else
      cmd = paste('retriever install', connection, dataset, '--file', db_file)
  }
  else if (connection == 'csv')
    cmd = paste('retriever install csv', dataset)
  else
    stop("The argument 'connection' must be set to one of the following options: 'mysql', 'postgres', 'sqlite', 'msaccess', or 'csv'")
  if (!is.null(log_dir)) {
    log_file = file.path(log_dir, paste(dataset, '_download.log', sep=''))
    cmd = paste(cmd, '>', log_file, '2>&1')
  }
  system(cmd)
}

#' Download datasets via the EcoData Retriever.
#'
#' Directly downloads data files with no processing, allowing downloading of
#' non-tabular data.
#'
#' @param dataset the name of the dataset that you wish to download
#' @param path the path where the data should be downloaded to
#' @param log_dir the location where the retriever log should be stored if
#' the progress is not printed to the console
#' @export
#' @examples
#' download_data('MCDB', './data')
download_data = function(dataset, path='.', log_dir=NULL) {
    cmd = paste('retriever download', dataset, '-p', path)
    if (!is.null(log_dir)) {
        log_file = file.path(log_dir, paste(dataset, '_download.log', sep=''))
        cmd = paste(cmd, '>', log_file, '2>&1')
    }
    system(cmd)
}


#' Update the scripts the EcoData Retriever uses to download datasets 
#'
#' @return returns the log of the Retriever's update
#' @references http://ecodataretriever.org/cli.html
#' @export
#' @examples update_scripts()
update_scripts = function() {
  system('retriever update') 
}

#' Display a list all available dataset scripts
#' @return returns the log of the available datasets for download
#' @export
#' @examples data_ls()
data_ls = function(){
  system('retriever ls') 
}

#' Create a new sample retriever script 
#' 
#' @param filename the name of the script to generate
#' @export
#' @examples new_script('newscript.script')
new_script = function(filename){
  system(paste('retriever new', filename)) 
}

