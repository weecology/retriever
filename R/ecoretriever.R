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
#' @param conn_file the path to the .conn file that contains the connection
#' configuration options for mysql and postgres databases. This defaults to 
#' mysql.conn or postgres.conn respectively. The connection file is a comma
#' seperated file with four fields: user, password, host, and port. 
#' @param data_dir the location where the dataset should be installed.
#' Only relevant for csv connection types. Defaults to current working directory
#' @param log_dir the location where the retriever log should be stored if
#' the progress is not printed to the console
#' @export
#' @examples
#' \donttest{
#' ecoretriever::install('MCDB', 'csv')
#' }
install = function(dataset, connection, db_file=NULL, conn_file=NULL,
                   data_dir='.', log_dir=NULL){ 
  if (missing(connection)) {
    stop("The argument 'connection' must be set to one of the following options: 'mysql', 'postgres', 'sqlite', 'msaccess', or 'csv'")
  }
  else if (connection == 'mysql' | connection == 'postgres') {
    if (is.null(conn_file)) {
      conn_file = paste('./', connection, '.conn', sep='')
    }
    if (!file.exists(conn_file)) {
      format = '\n    host my_server@myhost.com\n    port 1111\n    user my_user_name\n    password my_pass_word'
      stop(paste("conn_file:", conn_file, "does not exist. To use a",
                  connection, "server create a 'conn_file' with the format:", 
                 format, "\nwhere order of arguments does not matter"))
    }
    conn = data.frame(t(utils::read.table(conn_file, row.names=1)))
    writeLines(strwrap(paste('Using conn_file:', conn_file,
                             'to connect to a', connection,
                             'server on host:', conn$host)))
    cmd = paste('retriever install', connection, dataset, '--user', conn$user,
                '--password', conn$password, '--host', conn$host, '--port',
                conn$port)
  }
  else if (connection == 'sqlite' | connection == 'msaccess') {
    if (is.null(db_file))
      cmd = paste('retriever install', connection, dataset)
    else
      cmd = paste('retriever install', connection, dataset, '--file', db_file)
  }
  else if (connection == 'csv') {
    cmd = paste('retriever install csv --table_name',
                  file.path(data_dir, '{db}_{table}.csv'), dataset)
  }
  else
    stop("The argument 'connection' must be set to one of the following options: 'mysql', 'postgres', 'sqlite', 'msaccess', or 'csv'")
  if (!is.null(log_dir)) {
    log_file = file.path(log_dir, paste(dataset, '_download.log', sep=''))
    cmd = paste(cmd, '>', log_file, '2>&1')
  }
  system(cmd)
}

#' Fetch a dataset via the EcoData Retriever
#'
#' Each datafile in a given dataset is downloaded to a temporary directory and
#' then imported as a data.frame as a member of a named list.
#'
#' @param dataset the name of the dataset that you wish to download
#' @param quiet logical, if true retriever runs in quiet mode
#' @export
#' @examples
#' \donttest{
#' ## fetch the Mammal Community Database (MCDB)
#' MCDB = ecoretriever::fetch('MCDB')
#' class(MCDB)
#' names(MCDB)
#' ## preview the data in the MCDB communities datafile
#' head(MCDB$communities)
#' }
fetch = function(dataset, quiet=TRUE){
  temp_path = tempdir()
  if (quiet)
    system(paste('retriever -q install csv --table_name',
                 file.path(temp_path, '{db}_{table}.csv'),
                 dataset))
  else
    install(dataset, connection='csv', data_dir=temp_path)
  files = dir(temp_path)
  files = files[grep(dataset, files)]
  out = vector('list', length(files))
  list_names = sub('.csv', '', files)
  list_names = sub(paste(dataset, '_', sep=''), '', list_names)
  names(out) = list_names
  for (i in seq_along(files))
    out[[i]] = utils::read.csv(file.path(temp_path, files[i]))
  return(out)
}

#' Download datasets via the EcoData Retriever.
#'
#' Directly downloads data files with no processing, allowing downloading of
#' non-tabular data.
#'
#' @param dataset the name of the dataset that you wish to download
#' @param path the path where the data should be downloaded to
#' @param sub_dir if true and the downloaded dataset is stored in subdirectories those subdirectories will be preserved and placed according the path argument, defaults to false.
#' @param log_dir the location where the retriever log should be stored if
#' the progress is not printed to the console
#' @export
#' @examples 
#' \donttest{
#' ecoretriever::download('MCDB')
#' ## list files downloaded
#' dir('.', pattern='MCDB')
#' }
download = function(dataset, path='.', sub_dir=FALSE, log_dir=NULL) {
    if (sub_dir)
        cmd = paste('retriever download', dataset, dataset, '-p', path, '--subdir')
    else 
        cmd = paste('retriever download', dataset, '-p', path)
    if (!is.null(log_dir)) {
        log_file = file.path(log_dir, paste(dataset, '_download.log', sep=''))
        cmd = paste(cmd, '>', log_file, '2>&1')
    }
    system(cmd)
}

#' Name all available dataset scripts.
#'
#' Additional information on the available datasets can be found at http://ecodataretriever.org/available-data.html
#' 
#' @return returns a character vector with the available datasets for download
#' @export
#' @examples 
#' \donttest{
#' ecoretriever::datasets()
#' }
datasets = function(){
  system('retriever ls', intern = TRUE) 
}

#' Update the retriever's dataset scripts to the most recent versions.
#' 
#' This function will check if the version of the retriever's scripts in your local
#' directory \file{~/.retriever/scripts/} is up-to-date with the most recent official
#' retriever release. Note it is possible that even more updated scripts exist
#' at the retriever repository \url{https://github.com/weecology/retriever/tree/master/scripts}
#' that have not yet been incorperated into an official release, and you should 
#' consider checking that page if you have any concerns. 
#' @keywords utilities
#' @export
#' @examples
#' \donttest{
#' ecoretriever::get_updates()
#' }
get_updates = function() {
    writeLines(strwrap('Please wait while the retriever updates its scripts, ...'))
    update_log = system('retriever update', intern=TRUE, ignore.stdout=FALSE,
                        ignore.stderr=TRUE)
    writeLines(strwrap('The retriever scripts are up-to-date with the most recent official release!'))
    class(update_log) = "update_log"
    return(update_log)
}

#' @export
print.update_log = function(x, ...) {
    if (length(x) == 0) {
        cat('No scripts downloaded')
    } 
    else {
        # clean up and print the update log output
        object = strsplit(paste(x, collapse = ' ; '), 'Downloading script: ')
        object = sort(sapply(strsplit(object[[1]][-1], ' ; '), 
                       function(x) x[[1]][1]))
        object[1] = paste('Downloaded scripts:', object[1])
        cat(object, fill=TRUE, sep=', ')
    }
}

.onAttach = function(...) {
    packageStartupMessage(
        "\n  Use get_updates() to download the most recent release of download scripts
     
    New to ecoretriever? Examples at
      https://github.com/ropensci/ecoretriever/
      Use citation(package='ecoretriever') for the package citation
    \nUse suppressPackageStartupMessages() to suppress these messages in the future")
}

.onLoad = function(...) {
    check_for_retriever()
}

check_for_retriever = function(...) {
    retriever_path = Sys.which('retriever')
    if (retriever_path == '') {
        path_warn = 'The retriever is not on your path and may not be installed.'
        mac_instr = 'Follow the instructions for installing and manually adding the EcoData Retriever to your path at http://ecodataretriever.org/download.html'
        download_instr = 'Please upgrade to the most recent version of the EcoData Retriever, which will automatically add itself to the path http://ecodataretriever.org/download.html'
        os = Sys.info()[['sysname']]
        if (os == 'Darwin')
            packageStartupMessage(paste(path_warn, mac_instr))
        else 
            packageStartupMessage(paste(path_warn, download_instr))
    }    
}
