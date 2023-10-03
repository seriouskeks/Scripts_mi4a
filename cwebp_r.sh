#!/bin/bash
# based on an orginal idea by https://gist.github.com/tabrindle/ed9f77b4e96f4c98b49b

usage() {
  echo "Usage: web_img_export.sh [--verbose] [--sizes 300w,600h,...] [--dryrun] cwebp_params FILE_OR_DIRECTORY"

  exit
}

### General flags
FLAG_DRYRUN=0
FLAG_VERBOSE=0

### Global Variables
NEW_SIZES=()
ARGS=()

verbose() {
  if [ $FLAG_VERBOSE -eq 1 ]; then
    echo $1;
  fi
}

main() {
  resolve_flags $@

  local FILES
  echo "${@}"
  list_files FILES "${!#}"

  verbose "${#FILES[@]} files to process"

  shopt -s nullglob nocaseglob extglob

  for FILE in "${FILES[@]}"; do
    verbose "Processing $FILE"
    process_file "$FILE"
  done

  verbose "${#FILES[@]} files processed"
}

resolve_flags() {
  ## Looking is multiple sizes were provided
  if [ $# -ne 0 ]; then
    for ((i=1; i<$#; i++)) do
      case ${!i} in
        "--sizes")
          iplus=$(( i + 1 ))
          if [[ ${!iplus} =~ ^([0-9]+(w|h))(,[0-9]+(w|h))*$ ]]; then
            mapfile -td \, NEW_SIZES < <(printf "%s\0" "${!iplus}")

            verbose "Requested resize to: ${NEW_SIZES[@]}"

            i=$((i+1))
          else
            usage
          fi
        ;;

        "--dryrun")
          FLAG_DRYRUN=1
        ;;

        "--verbose")
          FLAG_VERBOSE=1
        ;;

        *)
          ARGS+=(${!i})
        ;;
      esac
    done
  fi
}

list_files() {
  local -n RESULT=$1

  FILE=$2
  echo $FILE
  OIFS="$IFS"

  IFS=$'\n'
  RESULT=($(find $FILE -iregex '.*\.\(jpg\|jpeg\|tif\|tiff\|png\)'))
  IFS="$OIFS"
}

size_to_dimensions() {
  SIZE=$1

  if [[ $SIZE =~ ^[0-9]+w$ ]]; then
    echo "${SIZE::-1} 0"
  else
    echo "0 ${SIZE::-1}"
  fi
}

process_file() {
  FILE=$1
  NAME=${FILE%.*}
  FLAT_ARGS="${ARGS[@]}"

  if [ ${#NEW_SIZES[@]} -ne 0 ]; then
    for SIZE in "${NEW_SIZES[@]}"; do
      DIMENS=$(size_to_dimensions $SIZE)

      NEWFILE="$NAME-$SIZE.webp"
      verbose "Resizing to $SIZE"

      verbose "cwebp $FLAT_ARGS -resize $DIMENS $FILE -o $NEWFILE"

      if [ $FLAG_DRYRUN -eq 0 ]; then
        cwebp $FLAT_ARGS -resize $DIMENS "$FILE" -o "$NEWFILE"
      fi
    done
  else
    verbose "cwebp $FLAT_ARGS $FILE -o $NAME.webp"

    if [ $FLAG_DRYRUN -eq 0 ]; then
      cwebp $FLAT_ARGS "$FILE" -o "$NAME.webp"
    fi
  fi
}

main "$@"
