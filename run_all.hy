(import collection aggregation analysis visualization)

(defn collect-data []
  (.run collection))

(defn aggregate-data []
  (.run aggregation))

(defn analyze-data []
  (.run analysis))

(defn generate-plots []
  )

(defn generate-reports []
  )

(defn run []
  (collect-data)
  (aggregate-data)
  (analyze-data))
